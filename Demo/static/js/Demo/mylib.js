$(document).ready(function(){
    $('#password1, #password2').on('keyup', function () {
    if ($('#password1').val() == $('#password2').val()) {
        $('#message').html('<b>Password Matching</b>').css('color', 'green');
    } else 
        $('#message').html('<b>Password Not Matching</b>').css('color', 'red');
    });
   $( function() {
    $( "#datepicker1" ).datepicker();
   });
   
   $( function() {
    $( "#datepicker2" ).datepicker();
   });

});

function submitOrgRegistry (){
    var data1 = null;
    var myJSON = null;
    if (document.getElementById('password1').value ==
          document.getElementById('password2').value) {
            if(document.getElementById('password1').value.length < 4){
                $('#message').html('<b>Password should be minimum 4 characters</b>').css('color', 'red');    
            }else{
                var url = '/orgRegistry/' ;
                paramJson = {
                        'csrfmiddlewaretoken':document.getElementById('csrfmiddlewaretoken').value,
                        'orgName' : document.getElementById('orgName').value,
                        'orgAdress' : document.getElementById('orgAdress').value,
                        'orgPhone' : document.getElementById('orgPhone').value,
                        'orgEmail' : document.getElementById('orgEmail').value,
                        'password' : document.getElementById('password1').value
                }
            
                $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                    $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );
            }
    }else{
        $('#message').html('<b>Retry..Password Not Matching</b>').css('color', 'red');
    }
}

function addReservation(){
    paramJson = {
                        'csrfmiddlewaretoken':document.getElementById('csrfmiddlewaretoken').value,
                        'fromDate' : document.getElementById('datepicker1').value,
                        'toDate' : document.getElementById('datepicker2').value,
                        'bookId' : document.getElementById('bookId').value,
                        'bookCopyCode' : document.getElementById('bookCopyCode').value,
                        'bookCopyId' : document.getElementById('bookCopyId').value
                };
                //alert (JSON.stringify(paramJson));
                $.post('/bookList/copies/reserve/',paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                       $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );
}

function submitUserAdd(){
    var data1 = null;
    var myJSON = null;
    if (document.getElementById('password1').value ==
          document.getElementById('password2').value) {
            if(document.getElementById('password1').value.length < 4){
                $('#message').html('<b>Password should be minimum 4 characters</b>').css('color', 'red');    
            }else{
                var url = '/userAdd/' ;
                paramJson = {
                        'csrfmiddlewaretoken':document.getElementById('csrfmiddlewaretoken').value,
                        'orgCode' : document.getElementById('orgCode').value,
                        'firstName' : document.getElementById('firstName').value,
                        'lastName' : document.getElementById('lastName').value,
                        'userPhone' : document.getElementById('userPhone').value,
                        'userEmail' : document.getElementById('userEmail').value,
                        'userAdress' : document.getElementById('userAdress').value,
                        'password' : document.getElementById('password1').value
                }
            
                $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                    $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );
            }
    }else{
        $('#message').html('<b>Retry..Password Not Matching</b>').css('color', 'red');
    }
}

function submitLibUserAdd(){
    var url = '/user/' ;
    paramJson = {
                'csrfmiddlewaretoken':document.getElementById('csrfmiddlewaretoken').value,
                'firstName' : document.getElementById('firstName').value,
                'lastName' : document.getElementById('lastName').value,
                'userPhone' : document.getElementById('userPhone').value,
                'userEmail' : document.getElementById('userEmail').value,
                'userAdress' : document.getElementById('userAdress').value
                }
            
                $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                    $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );
}



function userLogin(){
    paramJson = {
        'csrfmiddlewaretoken': document.getElementById('csrfmiddlewaretoken').value,
        'orgCode' : document.getElementById('orgCode').value,
        'userPin' : document.getElementById('userPin').value,
        'password' :  document.getElementById('password').value
    };
    var url = '/login/' ;
    $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#disp').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                        window.location.href = '/main/' ;
                    }
                },
                "json"
                );
}

function makeVisibleSubCategoryAdd(){
    document.getElementById('subCategoryModFromDisp').style.display="none";
    document.getElementById('subCategoryAddFromDisp').style.display="block";
}

function showCategoryAddForm(){
    $("#stalePageContent").empty();
    $.get('/showCategoryAddForm/',null, function(data, status,jqXHR){
                    $('#catShow').html(data);
                },
                "html"
    );
}

function addBook(){
    paramJson = {
        'bookName': document.getElementById('bookName').value,
        'author': document.getElementById('author').value,        
        'publisher': document.getElementById('publisher').value,
        'isbn': document.getElementById('isbn').value,
        'remark': document.getElementById('remark').value,
        'is_cd': document.getElementById('is_cd').value,
        'copies': document.getElementById('copies').value,
        'subCategoryId': document.getElementById('subCategoryId').value,
        'categoryId' : document.getElementById('categoryId').value,
        'csrfmiddlewaretoken': document.getElementById('csrfmiddlewaretoken').value
    };
    var url = '/book/' ;
    $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );
}

function getRemainingBookFrom (){
    $("#stalePageContent").empty();
    categoryId = document.getElementById('categoryId').value;
    subCategoryId  = document.getElementById('subCategoryId').value;
    url = '/book?op=getBookFrom&categoryId=' + categoryId + '&subCategoryId=' + subCategoryId;
    $.get(url,null, function(data, status,jqXHR){
                        $('#showRemainings').html(data);
                },
                "html"
                );
}

function getSubCategoryOfCategory(){
    $("#stalePageContent").empty();
    categoryId = document.getElementById('categoryId').value;
    url = '/book?op=getSubCategoryFrom&categoryId=' + categoryId;
    $.get(url,null, function(data, status,jqXHR){
                        $('#showSubCategory').html(data);
                },
                "html"
                );
}

function addSubCategory (){
    //document.getElementById('subCategoryModFromDisp').style.display="none";
    paramJson = {
        'csrfmiddlewaretoken': document.getElementById('csrfmiddlewaretoken').value,
        'orgCode' : document.getElementById('orgCode').value,
        'subcategory' : document.getElementById('subcategory').value,
        'categoryId' : document.getElementById('categoryId').value
    };   
    url = '/subCategory/';
    $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#subcategoryDisp').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else{
                         window.location.href = '/subCategory?'  + 'categoryId=' + paramJson['categoryId']  + '&orgCode=' + paramJson['orgCode']
                    }
                },
                "html"
                );
}


function submitCategoryAdd (){
    if (document.getElementById('category').value == ''){
         $('#message').html('<b>' +  'Nothing Entered' +  '</b>').css('color', 'red');
        return false;
    }
    paramJson = {
        'csrfmiddlewaretoken': document.getElementById('csrfmiddlewaretoken').value,
        'orgCode' : document.getElementById('orgCode').value,
        'category' : document.getElementById('category').value
    };
    var url = '/showCategoryAddForm/' ;
    $.post(url,paramJson, function(data, status,jqXHR){
                    if ( data['status'] == 'ERROR'){
                        $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'red');
                    }else if ( data['status'] == 'SUCCESS'){
                         $('#message').html('<b>' +  data['message'] +  '</b>').css('color', 'green');
                    }
                },
                "json"
                );    
}