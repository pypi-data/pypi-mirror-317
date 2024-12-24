'''function plainText = caesar_decipher(cipherText, key)
    % Convert cipherText to uppercase  
    cipherText = upper(cipherText);
    plainText = '';
    % Shift letters in the alphabet, ignoring non-alphabet characters
    for i = 1 : length(cipherText)
        chr = cipherText(i);
        if isletter(chr)
            shiftedChar = chr - key;
            if shiftedChar > 'Z'
                shiftedChar = shiftedChar - 26;
            elseif shiftedChar < 'A'
                shiftedChar = shiftedChar + 26;
            end
            plainText = [plainText, shiftedChar];
        else
            plainText = [plainText, chr];
        end
    end
end'''