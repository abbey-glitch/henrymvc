dashDisp = document.getElementById("dashcont")
let movieForm = document.createElement("div")
$("#men-title").on("click", function() {
    // alert("hello")
    dashDisp.innerHTML = `<form action="" method="post" enctype="multipart/form-data">
    <fieldset>
        <legend>Add Movie</legend>
        <input type="file" name="movie" id="movie">
        <br>
        <input type="text" name="movie-title" id="name" placeholder="Name">
        <br>
        <textarea col_span="2" name="movie-desc" id="desc"></textarea>
        <input type="submit" value="Upload">
    </fieldset>
    </form>`
    console.log(dashDisp);
});