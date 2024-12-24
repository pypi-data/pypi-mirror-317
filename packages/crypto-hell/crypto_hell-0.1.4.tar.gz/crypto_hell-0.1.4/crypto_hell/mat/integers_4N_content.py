# Auto-generated file for integers_4N.m
file_content = '''
% Example usage
integers_to_4N(10);
integers_to_4N(20);
integers_to_4N(30);
integers_to_4N(40);

function integers_to_4N(N)
sequence=zeros(1,N);
for i=1:N
    sequence(i) = 4*i;
end
    disp(['Integers from 4 to 4N for N = ', num2str(N), ':']);
    disp(sequence);
function T = compute_T(n)
    % Base case
    if n == 0
        T = 1;
    else
        % Recursive case
        T = 3 * compute_T(n - 1);
    end
end


'''
