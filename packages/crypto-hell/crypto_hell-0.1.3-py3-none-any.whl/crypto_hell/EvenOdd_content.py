# Auto-generated file for EvenOdd.m
file_content = '''
% Example usage
disp('For N = 10:');
modified_numbers(10);

disp('For N = 20:');
modified_numbers(20);

disp('For N = 40:');
modified_numbers(40);

function modified_numbers(N)
    result = zeros(1, N);

    for i = 1:N
        if mod(i, 2) == 1 % Odd number
            result(i) = i + 1;
        else % Even number
            result(i) = i - 1;
        end
    end

    % Display the result
    disp(['Modified numbers for N = ', num2str(N), ':']);
    disp(result);
end


'''
