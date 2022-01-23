<?php

$cipher_text = 'FEAjLtaf9bQ7oJCY53mV3IJOWDVi7donm6KEb9yjsxkCjuz0gpluD1vczeQGb8Pg';
$key = 296332286;

$plain_text = openssl_decrypt($cipher_text, 'AES-128-ECB', $key);

echo $plain_text

?>