<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload</title>
</head>
<body>
    <h2>Upload File</h2>
    <form action="upload.php" method="post" enctype="multipart/form-data">
        Select file to upload:
        <input type="file" name="fileToUpload" id="fileToUpload">
        <input type="submit" value="Upload File" name="submit">
    </form>
    <?php
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $target_dir = "uploads/";
        $file_name = basename($_FILES["fileToUpload"]["name"]);
        $target_file = $target_dir . $file_name;
        $uploadOk = 1;

        // Check file size
        if ($_FILES["fileToUpload"]["size"] > 500000) {
            echo "Sorry, your file is too large.";
            $uploadOk = 0;
        }

        // Allow certain file formats
        $file_type = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));
        $allowed_types = ['jpg', 'png', 'gif', 'pdf'];
        if (!in_array($file_type, $allowed_types)) {
            echo "Sorry, only JPG, PNG, GIF, & PDF files are allowed.";
            $uploadOk = 0;
        }

        // Check if $uploadOk is set to 0 by an error
        if ($uploadOk == 0) {
            echo "Sorry, your file was not uploaded.";
        } else {
            // Sanitize file name
            $safe_file_name = preg_replace('/[^a-zA-Z0-9-_\.]/', '', $file_name);
            $target_file = $target_dir . $safe_file_name;

            if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
                echo "The file ". htmlspecialchars($safe_file_name). " has been uploaded.";
            } else {
                echo "Sorry, there was an error uploading your file.";
            }
        }
    }
    ?>
</body>
</html>
