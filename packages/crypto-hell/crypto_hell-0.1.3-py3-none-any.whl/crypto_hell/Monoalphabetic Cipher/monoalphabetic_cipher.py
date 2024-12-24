'''function cipherText = monoalphabetic_cipher(plainText, key)
    % Convert plainText to uppercase   
    plainText = upper(plainText);
    cipherText = '';
    % Define the alphabet
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    % Encrypt each character
    for i = 1 : length(plainText)
        chr = plainText(i);
        if isletter(chr)
            % Find the position of the character in the alphabet
            index = find(alphabet == chr);
            % Substitute using the key
            cipherText = [cipherText, key(index)];
        else
            % Non-letter characters are added as is
            cipherText = [cipherText, chr];
        end
    end
end'''