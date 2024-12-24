'''function cipherText = caesar_cipher(plainText, key)
    % Convert plainText uppercase
    plainText = upper(plainText);
    cipherText = '';
    % Shift letters in the alphabet, ignoring non-alphabet characters
    for i = 1 : length(plainText)
        chr = plainText(i);
        if isletter(chr)
            shiftedChar = chr + key;
            if shiftedChar > 'Z'
                shiftedChar = shiftedChar - 26;
            elseif shiftedChar < 'A'
                shiftedChar = shiftedChar + 26;
            end
            cipherText = [cipherText, shiftedChar];
        else
            cipherText = [cipherText, chr];
        end
    end
end'''