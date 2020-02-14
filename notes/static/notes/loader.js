var send_data = {}
var csrftoken = Cookies.get('csrftoken')
function resetFilters() {
    send_data['sort_by'] = ''
    send_data['format'] = 'json'
}

function putData(result) {
    let col;
    let svgBookmark = "<svg class=\"bi bi-bookmark-fill float-right\" width=\"2.5em\" height=\"2.5em\" viewBox=\"0 0 20 20\"" +
        "fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">" +
        "<path fill-rule=\"evenodd\" d=\"M5 5a2 2 0 012-2h6a2 2 0 012 2v12l-5-3-5 3V5z\" clip-rule=\"evenodd\" />" +
        "</svg>"
    let svgEyeFill = "<svg class=\"bi bi-eye-fill float-right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 20 20\" fill=\"currentColor\"" +
        "xmlns=\"http://www.w3.org/2000/svg\">" +
        "<path d=\"M12.5 10a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z\" />" +
        "<path fill-rule=\"evenodd\"" +
        "d=\"M2 10s3-5.5 8-5.5 8 5.5 8 5.5-3 5.5-8 5.5S2 10 2 10zm8 3.5a3.5 3.5 0 100-7 3.5 3.5 0 000 7z\"" +
        "clip-rule=\"evenodd\" />" +
        "</svg>"
    let svgEyeSlash = "<svg class=\"bi bi-eye-slash-fill float-right\" width=\"2em\" height=\"2em\" viewBox=\"0 0 20 20\"" +
        "fill=\"currentColor\" xmlns=\"http://www.w3.org/2000/svg\">" +
        "<path " +
        "d=\"M12.79 14.912l-1.614-1.615a3.5 3.5 0 01-4.474-4.474l-2.06-2.06C2.938 8.278 2 10 2 10s3 5.5 8 5.5a7.027 7.027 0 002.79-.588zM7.21 5.088A7.028 7.028 0 0110 4.5c5 0 8 5.5 8 5.5s-.939 1.72-2.641 3.238l-2.062-2.062a3.5 3.5 0 00-4.474-4.474L7.21 5.088z\" />" +
        "<path " +
        "d=\"M7.525 9.646a2.5 2.5 0 002.829 2.829l-2.83-2.829zm4.95.708l-2.829-2.83a2.5 2.5 0 012.829 2.829z\" />" +
        "<path fill-rule=\"evenodd\" d=\"M15.646 16.354l-12-12 .708-.708 12 12-.708.707z\" clip-rule=\"evenodd\" />" +
        "</svg>"
    $("#row").html("");
    if (result.length > 0) {        
        $.each(result, function (i, v) {
            col = "<div class=\"col-md-3\">" +
                "<div class=\"col-md-12 shadow-sm bg-light p-2 mb-4 text-break\">"
            if (v.bookmark == true) {
                col += svgBookmark
            }
            col += "<h3>" + v.title + "</h3>"
            col += "<p class=\"badge badge-primary\">" + v.category_title + "</p>"
            col += "<p class=\"badge badge-primary\">" + v.dtcreate + "</p>"
            col += "<p>" + v.context + "</p>"
            col += "<button class=\"btn btn-sm btn-info\" id=\"detailbtn\" onclick=\"getNoteData('" + v.uuid + "')\">Details</button>"
            if (v.published) {
                col += svgEyeFill
            }
            else {
                col += svgEyeSlash
            }
            col += "</div></div>"
            $("#row").append(col)
        });
    }
}

async function getAPIData() {
    let url = new URL(window.location.origin + '/notes/api/notes')
    url.search = new URLSearchParams(send_data).toString()
    let response = await fetch(url, {
        method: 'GET',
        headers:{
            "Accept": "application/json",
            "X-CSRFToken": csrftoken
        }
    });
    if (response.ok) {
        data = await response.json()
        putData(data)
    }
    else {
        console.log('http error: ' + response.status)
    }
}

async function getNoteData(uuid) {
    let url = window.location.origin + '/notes/api/notes/' + uuid
    let response = await fetch(url, {
        method: 'GET',
        headers:{
            "Accept": "application/json",
            "X-CSRFToken": csrftoken
        }
    });
    data = await response.json()
    drawNoteModal(data["title"], data["context"], data["uuid"], data["category"], data["published"], data["bookmark"])
}

function drawNoteModal(title, body, uuid, category, published, bookmark) {
    $("#noteLabel").val(title);
    $("#openbtn").prop('href', uuid);
    $("#noteContext").html(body);
    $("#catSelector").val(category)    
    $("#noteUUID").html(uuid);    
    $('#deletebtn').prop('value', uuid);    
    $('#published').prop('checked', published);
    $('#bookmark').prop('checked', bookmark);
    $('#modalNote').modal('show')
}

async function drawCategories() {
    let url = window.location.origin + '/notes/api/categories'
    let response = await fetch(url, {
        method: 'GET',
        headers:{
            "Accept": "application/json",
            "X-CSRFToken": csrftoken
        }
    });
    data = await response.json()
    $.each(data, function (i, v) {
        $("#catSelector").append("<option value =\"" + v.id + "\">" + v.title + "</option> ")
        $("#catFilter").append("<option value =\"" + v.id + "\">" + v.title + "</option> ")
    })
}

async function updateNote() {    
    let uuid = $("#noteUUID").text()    
    let title = $("#noteLabel").val();
    let category = $("#catSelector").val();
    let context = $("#noteContext").val();    
    let published = $('#published').prop('checked');
    let bookmark = $('#bookmark').prop('checked');    

    note_body = {
        title: title,
        context: context,
        category: category,
        bookmark: bookmark,
        published: published
    }
    let method;
    let url;
    if (uuid) {
        method = 'PUT'
        url =  window.location.origin + '/notes/api/notes/' + uuid
    }
    else {
        method = 'POST'
        url =  window.location.origin + '/notes/api/notes/create'
    }    
    let response = await fetch(url, {
        method: method,
        headers:{
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(note_body)
    });
    $('#modalNote').modal('hide');
    if (response.ok) {        
        drawAlert('Ok', 'successfuly save')
        getAPIData();
    }
    else {
        data = await response.text()
        drawAlert(response.status, data)
    }
}

async function deleteNote() {
    let url =  window.location.origin + '/notes/api/notes/' + $("#noteUUID").text()    
    let response = await fetch(url, {
        method: 'DELETE',
        headers:{
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },        
    });
    if (response.ok) {        
        drawAlert('Ok', 'successfuly delete')
        getAPIData();
        $('#modalNote').modal('hide');

    }
    else {
        data = await response.text()
        drawAlert(response.status, data)
    }
}

function drawAlert(title, body) {
    $("#alertTitle").html(title)
    $("#alertBody").html(body)
    $('#modalAlert').modal('show')
}

function search() {    
    send_data["title"] = $('#searchinp').val();    
    send_data["category"] = $('#catFilter').val();   
    send_data["bookmark"] = $('#bookmarkFilter').val();    
    send_data["dtcreate"] = $('#dtcreateFilter').val();
    send_data["sort_by"] = $('#sortbyFilter').val();
    getAPIData();
}

function createNote() {
    $("#noteUUID").text('')
    $("#noteUUID").hide();
    $("#openbtn").hide();
    $("#noteLabel").val('');
    $("#noteContext").val('');
    $("#catSelector").val(1);    
    $('#published').prop('checked', false);
    $('#bookmark').prop('checked', false); 
    $('#deletebtn').hide();
    $('#modalNote').modal('show');
}