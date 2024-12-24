'''function cipherText = rail_fence_cipher(plainText, depth)
    % Initialize an empty character array for the rails with specified depth
    rail = char(zeros(depth, length(plainText)));
    % Start at the first row and set the initial direction to "down" (1)
    row = 1;
    direction = 1; % 1 for moving down, -1 for moving up
    % Iterate over each character in the plain text
    for i = 1:length(plainText)
        % Place the current character in the appropriate row and column
        rail(row, i) = plainText(i);
        % Change direction at the top or bottom rail
        if row == 1
            direction = 1; % start moving down
        elseif row == depth
            direction = -1; % start moving up
        end
        % Move to the next row according to the current direction
        row = row + direction;
    end
    % Reshape the rail matrix to a single row and remove empty (zero) characters
    rail = reshape(rail.', 1, []);
    cipherText = rail(rail ~= 0); % remove zeros (empty spaces)
end'''