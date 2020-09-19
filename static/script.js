function ShowVarSelection() {
    var variant = document.getElementById("var");
    var selectVar = document.getElementById("selectVar");
    selectVar.style.display = variant.checked ? "block" : "none";
}
function ShowUploadMethod() {
    var method1 = document.getElementById("paste");
    var displayMethod1 = document.getElementById("textInputFile");
    displayMethod1.style.display = method1.checked ? "block" : "none";
    var method2 = document.getElementById("file");
    var displayMethod2 = document.getElementById("uploadInputFile");
    displayMethod2.style.display = method2.checked ? "block" : "none";
}
function ShowLoader() {
    var loader = document.getElementById("myloader");
    loader.style.display = "inline-block";
}
function validate() {
    if (document.getElementById("seq").checked || (document.getElementById("var").checked && document.getElementById("selectVar").value != '')) {
        if (document.getElementById("paste").checked) {
            if (document.getElementById("textInputFile").value != '') {
                ShowLoader();
                return true;
            } else {
                alert("input valid text")
                return false;
            }
            
        } else if (document.getElementById("file").checked) {
            if (document.getElementById("uploadInputFile").files.length == 0) {
                alert("no file selected");
                return false;
            } else {
                ShowLoader();
                return true;
            }
        } else {
            alert("input file");
            return false;
        }
    } else {
        alert("file type")
        return false;
    }
}
$(document).ready(function() {
    $('#result').DataTable();
} );
