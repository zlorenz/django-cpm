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
                    $('#task-category-list').prepend('<li><a href="' + data['update_url'] + '">' + $this_title + '</a><ul id="ul-category-' + data['pk'] + '"></ul></li>');
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

