"""function cipherText = vigenere_cipher(plainText, key)
    % Convert plainText and key to uppercase
    plainText = upper(plainText);
    key = upper(key);
    keyLength = length(key);
    cipherText = '';
    % Encrypt each character
    for i = 1 : length(plainText)
        chr = plainText(i);
        if isletter(chr)
            % Find positions in the alphabet (0-25)
            charIndex = double(chr) - double('A');
            keyChar = key(mod(i-1, keyLength) + 1);
            keyIndex = double(keyChar) - double('A');
            % Apply Vigenère cipher shift
            encryptedChar = mod(charIndex + keyIndex, 26) + double('A');
            cipherText = [cipherText, char(encryptedChar)];
        else
            % Non-letter characters are added as is
            cipherText = [cipherText, chr];
        end
    end
end"""