/**
 * goldhand
 * Date: 7/21/13
 * Time: 2:15 PM
 * To change this template use File | Settings | File Templates.
 */


var task_form_url;
var category_form_url;
var project_form_url;

var project_id;
var project_summary_json;

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('#task-category-list').sortable({
    axis: 'y',
    containment: 'parent',
    delay: 50,
    distance: 10,
});

$('#task-category-list').on("sortstop", function(event, ui) {
    var cats = [];
        var catList = $(this).sortable('toArray');
        var formCount = 0;
        for (var i =0; i < catList.length; i++) {

            var cat_id = catList[i].split('_')[1].split('=')[1];
            console.log(cat_id);
            var cat = {
                'id': cat_id,
                'title': project_summary_json[cat_id]['title_url'],
                //'title': project_summary_json['category_totals'][cat_id]['title_url'],
                'order': i
            };
            console.log(cat.title + ' : ' + cat.order);
            cats.push(cat);


            formCount += 1;
        }
        var cats_str = [];
        for (i=0; i < cats.length; i++) {
            var cat_keys = Object.keys(cats[i]);
            var prefix = 'form-' + i + '-';
            for (var a=0; a < cat_keys.length; a++) {
                cats_str.push(prefix + [cat_keys[a], cats[i][cat_keys[a]]].join('='));
            }
        }

        var cookie = 'csrfmiddlewaretoken=' + getCookie('csrftoken') + '&';
        var extraPost = 'form-MAX_NUM_FORMS=1000&form-TOTAL_FORMS=' + formCount + '&form-INITIAL_FORMS=' + formCount + '&';
        var ajaxPost = cookie + extraPost + cats_str.join('&');
        console.log(ajaxPost);
        $.ajax({ url: '/cpm/tasks/category/manage/',
            type: 'POST',
            data: ajaxPost,
           success: function (data) { console.log('success' + data['success']); },
           error: function (data) { console.log(data['error']); }
        })
    });


var data_list = [];
function getProjectSummary(project_id) {
    var JSON_url = '/cpm/projects/json/' + project_id + '/';
    var project_data = {};
    $.getJSON(JSON_url, function (data) {
        //project_summary_json = data;

        // $.each(data, function(key, value) {
        //   list_data.push('<li>' + key + ' : ' + value + '</li>');
        // });
        var i = 0;
        $.each(data['category_totals'], function(key, value) {
            var list1_data = [];
            var cat_title = value['title'];
            var cat_id = key;
            // TODO: Should be var cat_id = value['id'];
            var cat_order = value['order'];
            var cat_title_url = value['title_url'];

            $.each(value, function(key_1, value_1) {
                // list1_data.push('<li>' + key_1 + ' : ' + value_1 + '</li>');
            });
            $.each(value['task_set'], function(key_1, value_1) {
                var list2_data = [];
                var list2_title;
                $.each(value_1, function(key_2, value_2) {
                    list2_data.push('<li>' + key_2 + ' : ' + value_2 + '</li>');
                    if (key_2 == 'title') {
                        list2_title = value_2;
                    }
                });
                list1_data.push('<li>' + list2_title + '<ul>' + list2_data.join('') + '</ul></li>' );
            });
            project_data[key] = '<ul>' + list1_data.join('') + '</ul>';
            i++;
        });
        //$('#task-category-list').html(list_data.join(''));

    $.getJSON('/cpm/tasks/category/', function (data) {
        var list_data = [];
        project_summary_json = data;
        var project_summary_list = [];
        $.each(data, function(key, value) {
            project_summary_list.push(value);
        });
        project_summary_list = project_summary_list.sort(function (a, b) {if (a.order > b.order) return 1; if (a.order < b.order) return -1; return 0;});
        $.each(project_summary_list, function(key, value) {
            var list_item;
            if (project_data[value['id']]) {
                list_item = '<li id="cat_' + 'id=' + value['id'] +'"><a href="' + value['update_url'] + '">' + value['title'] + '</a>' + project_data[value['id']] + '</li>';
            } else {
                list_item = '<li id="cat_' + 'id=' + value['id'] +'"><a href="' + value['update_url'] + '">' + value['title'] + '</a></li>';
            }

            list_data.push(list_item);
        });
        $('#task-category-list').html(list_data.join(''));
        data_list = project_summary_list;


    })
    });



}

function getProjectForm(projectUrl) {
    $.getJSON(projectUrl, function (data) {
        $('#project-form').replaceWith(data['form_html']);
    })
}
function getTaskForm(taskUrl) {
    $.getJSON(taskUrl, function (data) {
        $('#task-form').replaceWith(data['form_html']);
    });
}
function getTaskCategoryForm(taskUrl) {
    $.getJSON(taskUrl, function (data) {
        $('#task-category-form').replaceWith(data['form_html']);
    });
}


function showStep(step) {
    if (step == 1) {
        $('#step-nav a[href="#new-project"]').tab('show');

    }
    else if (step == 2) {
        $('#step-nav a[href="#new-category"]').tab('show');
    }
    else {
        $('#step-nav a[href="#new-task"]').tab('show');
    }
}
$('#step-nav a[href="#new-project"]').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});
$('#step-nav a[href="#new-category"]').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});
$('#step-nav a[href="#new-task"]').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});


$('#form-wizard').on('submit', '#project-form', function (event) {
    event.preventDefault();
    var $this = $(this);
    console.log($this.serialize());
    var project_form_title = $this.find('#id_title').val();
    var cookie = 'csrfmiddlewaretoken=' + getCookie('csrftoken') + '&';

    if (project_form_title == "") {
        $this.find("#div_id_title").addClass('error');
        $(project_form_title).after('<span class="help-inline">Title required</span>');
        $(project_form_title).focus();
        return false;
    } else {
        $('.help-inline').remove();
        $("#div_id_title").removeClass('error');
    }
    $.ajax({
        url: project_form_url,
        type: "POST",
        data: cookie + $this.serialize(),
        success: function (data) {
            console.log(data['form_html']);
            if (!(data['success'])) {
                console.log('Fail');
                $this.replaceWith(data['form_html']);
            }
            else {
                project_form_url = data['update_url'];
                project_id = data['pk'];
                console.log('PID:  ' + data['pk']);
                //$('#new-project').find('.success-message').show(1000).hide(5000);
                showStep(2);
                $('#new-category input#id_title').focus();
            }
        },
        error: function () {
            $('#new-project').find('.error-message').show()
        }
    });
    return false;
});

$('#form-wizard').on('submit', '#task-category-form', function (event) {
    var $this = $(this);
    event.preventDefault();
    var $this_title = $this.find('#id_title').val();
    var this_url;
    var cookie = 'csrfmiddlewaretoken=' + getCookie('csrftoken') + '&';

    if (!$(this).attr('action')) {
        this_url = category_form_url;
    } else {
        this_url = $(this).attr('action');
    }

    console.log(cookie + $(this).serialize());
    $.ajax({
        url: this_url,
        type: "POST",
        data: cookie + $(this).serialize(),
        success: function (data) {
            if (!(data['success'])) {
                $this.replaceWith(data['form_html']);
            }
            else {
                $this.replaceWith(data['form_html']);
                // updates taskform with new category option
                getTaskForm(task_form_url);
                //$this.find('.success-message').show(1000).hide(5000);
                if ((data['new'])) {
                    $('#task-category-list').prepend(
                        '<li><a href="' + data['update_url'] + '">' + $this_title + '</a><ul id="ul-category-' + data['pk'] + '"></ul></li>');
                }
            }
        },
        error: function () {
            $this.find('.error-message').show()
        }
    });
    return false;
});

$('#form-wizard').on('submit', '#task-form', function (event) {
    event.preventDefault();
    var $task_form = $(this);
    var task_form_title = $task_form.find('#id_title').val();
    var task_form_category = $task_form.find('#id_category').val();
    var task_form_project = $task_form.find('#id_project');
    var task_url;
    var cookie = 'csrfmiddlewaretoken=' + getCookie('csrftoken') + '&';

    if (task_form_project.val() == "") {
        task_form_project.val(project_id);
    }

    if (!$(this).attr('action')) {
        task_url = task_form_url;
    } else {
        task_url = $(this).attr('action');
    }

    console.log(cookie + $(this).serialize());
    $.ajax({
        url: task_url,
        type: "POST",
        data: cookie + $(this).serialize(),
        success: function (data) {
            if (!(data['success'])) {
                $task_form.replaceWith(data['form_html']);
            }
            else {
                $task_form.replaceWith(data['form_html']);
                $task_form.find('.success-message').show(1000).hide(5000);
                if ((data['new'])) {
                    $('#ul-category-' + task_form_category).prepend('<li><a href="' + data['update_url'] + '">' + task_form_title + '</a></li>');
                }
                getProjectSummary(project_id);
            }
        },
        error: function () {
            $task_form.find('.error-message').show()
        }
    });
    return false;
});


$('#task-category-list').on('click', 'a', function (event) {
    event.preventDefault();
    var $this = $(this);
    $('#task-category-list li').removeClass('active');
    if ($this.is('[href*="category"]')) {
        showStep(2);
        getTaskCategoryForm($(this).attr('href'));
    }
    else {
        showStep(3);
        getTaskForm($(this).attr('href'));
    }
    $this.parent().addClass('active')
});

