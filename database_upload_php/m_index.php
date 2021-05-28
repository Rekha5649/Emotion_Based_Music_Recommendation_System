<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload_audio</title>
</head>
<body>
    <form action='upload.php' method='POST' enctype='multipart/form-data'>
        <input type='file' name = 'audioFile'/><br/><br/>
        <input type='text' value='Type Emotion' name = 'Emotion'/><br/><br/>
        <input type='text' value='Type Language' name = 'Language'/><br/><br/>
        <input type='text' value='Before - 1980s or 2010 - Present' name = 'Decade'/><br/><br/>
        <input type='submit' value='Upload Audio and Emotion' name='save_audio'/><br/><br/>
    </form>
</body>
</html>