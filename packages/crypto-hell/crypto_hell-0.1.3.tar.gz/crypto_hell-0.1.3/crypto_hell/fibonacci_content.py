# Auto-generated file for fibonacci.m
file_content = '''
% Example usage
fibonacci(10); 
function F = fibonacci(n)
    F = zeros(1, n);
    F(1) = 1; 
    F(2) = 1; 
    for i = 3:n
        F(i) = F(i-1) + F(i-2);
    end

    % Display the result
    disp(['First ', num2str(n), ' Fibonacci numbers:']);
    disp(F);
end



'''
