'''function cipherText = columnar_cipher(plainText, key)
    % Determine the number of columns based on the length of the key
    numCols = length(key);
    % Calculate the number of rows and pad the plaintext with 'X' if necessary
    numRows = ceil(length(plainText) / numCols);
    paddedLength = numRows * numCols;
    plainText = [plainText, repmat('X', 1, paddedLength - length(plainText))];
    % Create the columnar transposition matrix by reshaping the plaintext
    transpositionMatrix = reshape(plainText, numCols, numRows).';
    % Sort the columns based on the alphabetical order of the key
    [~, order] = sort(key);
    % Read columns in the order defined by the sorted key to build the ciphertext
    cipherText = ''; % Initialize ciphertext
    for i = 1:numCols
        cipherText = [cipherText, transpositionMatrix(:, order(i)).'];
    end
end'''