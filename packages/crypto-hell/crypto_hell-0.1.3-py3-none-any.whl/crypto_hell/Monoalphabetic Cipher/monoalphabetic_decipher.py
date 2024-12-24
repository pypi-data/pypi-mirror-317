'''function plainText = monoalphabetic_decipher(cipherText, key)
    % Convert cipherText to uppercase   
    cipherText = upper(cipherText);
    plainText = '';
    % Define the alphabet
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    % Decrypt each character
    for i = 1 : length(cipherText)
        chr = cipherText(i);
        if isletter(chr)
            % Find the position of the character in the alphabet
            index = find(key == chr);
            % Substitute using the key
            plainText = [plainText, alphabet(index)];
        else
            % Non-letter characters are added as is
            plainText = [plainText, chr];
        end
    end
end'''