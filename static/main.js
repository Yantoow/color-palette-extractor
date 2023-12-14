function addToPalette(col) {
    $.getJSON('/add_to_palette', {c: col});
}

function showLoadingGif() {
    document.getElementById("img-upload").setAttribute('src', "static/images/loading.gif");
    document.getElementById("img-upload").setAttribute('height', "50");
}