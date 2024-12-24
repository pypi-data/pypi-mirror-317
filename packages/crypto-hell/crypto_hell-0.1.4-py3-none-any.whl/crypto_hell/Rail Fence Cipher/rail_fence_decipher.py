'''function plainText = rail_fence_decipher(cipherText, depth)
    % Get the length of the ciphertext
    textLength = length(cipherText);
    % Initialize the rail matrix
    rail = char(zeros(depth, textLength));
    % Determine the zig-zag pattern of rows
    row = 1;
    direction = 1; % 1 for down, -1 for up
    pattern = zeros(1, textLength);
    for i = 1:textLength
        pattern(i) = row;
        if row == 1
            direction = 1; % change to down
        elseif row == depth
            direction = -1; % change to up
        end
        row = row + direction;
    end
    % Fill rail matrix with ciphertext characters based on pattern
    currentIndex = 1;
    for r = 1:depth
        for i = 1:textLength
            if pattern(i) == r
                rail(r, i) = cipherText(currentIndex);
                currentIndex = currentIndex + 1;
            end
        end
    end
    % Read plaintext from the rail matrix in zig-zag order
    plainText = '';
    for i = 1:textLength
        plainText = [plainText, rail(pattern(i), i)];
    end
end'''