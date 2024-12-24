'''function plainText = otp_decipher(cipherText, key)
    % Convert cipher text to uppercase numeric values (A = 0, B = 1, ...)
    cipherTextNum = double(upper(cipherText)) - double('A');
    % Convert key to uppercase numeric values
    keyNum = double(upper(key)) - double('A');
    % Decrypt by subtracting key from cipher text and wrapping with mod 26
    plainTextNum = mod(cipherTextNum - keyNum, 26);
    % Convert numeric values back to characters for the plain text
    plainText = char(plainTextNum + double('A'));
end'''