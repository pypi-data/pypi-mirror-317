'''function plainText = columnar_decipher(cipherText, key)
    % Convert the key to uppercase to ensure consistent sorting
    key = upper(key);
    % Calculate the number of columns and rows needed for the cipher grid
    numCols = length(key);
    numRows = ceil(length(cipherText) / numCols);
    % Get the order of columns based on sorting the key alphabetically
    [~, sortedIdx] = sort(key);
    % Initialize an empty grid to hold the transposed ciphertext
    grid = char(zeros(numRows, numCols));
    % Fill the grid column by column according to the order of the sorted key
    currentIndex = 1;
    for i = 1:numCols
        col = sortedIdx(i); % Get the correct column index based on the key
        for row = 1:numRows
            if currentIndex <= length(cipherText)
                grid(row, col) = cipherText(currentIndex);
                currentIndex = currentIndex + 1;
            end
        end
    end
    % Read the plaintext from the grid row by row
    plainText = '';
    for row = 1:numRows
        for col = 1:numCols
            if grid(row, col) ~= 0 % Ignore empty cells
                plainText = [plainText, grid(row, col)];
            end
        end
    end
end'''