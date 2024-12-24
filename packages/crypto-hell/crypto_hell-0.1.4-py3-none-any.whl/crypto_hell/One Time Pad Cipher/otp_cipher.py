'''function cipherText = otp_cipher(plainText, key)
    % Convert plain text to uppercase numeric values (A = 0, B = 1, ...)
    plainTextNum = double(upper(plainText)) - double('A');
    % Convert key to uppercase numeric values
    keyNum = double(upper(key)) - double('A');
    % Apply OTP cipher and wrap with mod 26
    cipherTextNum = mod(plainTextNum + keyNum, 26);
    % Convert numeric values back to characters
    cipherText = char(cipherTextNum + double('A'));
end'''