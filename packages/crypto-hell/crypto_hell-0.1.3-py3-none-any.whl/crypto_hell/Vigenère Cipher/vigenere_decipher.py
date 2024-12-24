"""function plainText = vigenere_decipher(cipherText, key)
    % Convert cipher and key to uppercase
    cipherText = upper(cipherText);
    key = upper(key);
    keyLength = length(key);
    plainText = '';
    % Decrypt each character
    for i = 1 : length(cipherText)
        chr = cipherText(i);
        if isletter(chr)
            % Find positions in the alphabet (0-25)
            charIndex = double(chr) - double('A');
            keyChar = key(mod(i-1, keyLength) + 1);
            keyIndex = double(keyChar) - double('A');
            % Apply Vigenère cipher shift
            encryptedChar = mod(charIndex - keyIndex, 26) + double('A');
            plainText = [plainText, char(encryptedChar)];
        else
            % Non-letter characters are added as is
            plainText = [plainText, chr];
        end
    end
end"""