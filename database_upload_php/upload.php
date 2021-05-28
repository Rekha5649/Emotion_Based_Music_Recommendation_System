<?php

if(isset($_POST['save_audio']) && $_POST['save_audio'] == 'Upload Audio and Emotion')
{
    $dir = 'uploads/';
    $audio_path = $_FILES['audioFile']['name'];

    if(move_uploaded_file($_FILES['audioFile']['tmp_name'], $audio_path))
    {
        echo 'uploaded succesfully';
        saveAudio($audio_path, $_POST['Emotion'], $_POST['Language'],$_POST['Decade'] );
    }
}

function saveAudio($Song_name, $Emotion, $Langue, $Decade)
{
    $servername = 'localhost';
    $username = 'root';
    $password = '';
    $database = 'MUSIC';

    $conn = mysqli_connect($servername, $username, $password, $database);
   
    if(!$conn)
    {
        die('server not connected');
    }

    echo '<br/>'.$Emotion.'<br/>';
    echo $Decade.'<br/>';
    echo $Song_name.'<br/>';
    
    $query = "INSERT INTO SONGS(Song_name, Emotion, Langue, Decade) VALUES('{$Song_name}', '{$Emotion}','{$Langue}', '{$Decade}')";
    

    $result = mysqli_query($conn, $query);

    echo '<br/>Result is: '.$result.'<br/>';
    echo '<br/>Affected rows are: '.mysqli_affected_rows($conn).'<br/>';

    if(mysqli_affected_rows($conn)>0)
    {
        echo 'audio file path saved in database.<br/>';
    }
    else{
        echo 'Data is not stored in Music database<br/>.';
    }

    if($result){
        echo 'Table created successfully<br/>';
    }
    else{
        echo "Problem<br/>".mysqli_error($conn);
    }

    mysqli_close($conn);
}

?>