# Auto-generated file for sum_Matrix_fact.m
file_content = '''
% Example usage
A = [-1, 0, 4, 10, 12;
      3, -7, -5, 5, 9;
      5, -5, -2, 0, 0;
      7, -3, 3, -2, 6;
      9,  4, 8,  4, 1];

x = 0.1;
y = 0.4;

% Compute for N = 3
compute_sum(A, x, y, 3);
% Compute for N = 4
compute_sum(A, x, y, 4);
% Compute for N = 5
compute_sum(A, x, y, 5);

function S = compute_sum(A, x, y, N)
    S = 0;
    for i = 1:N
        for j = 1:i
            term = A(i, j) * (x^i) * (y^j) / (fact(i) * fact(j)); 
            S = S + term; %
        end
    end
    disp(['Sum for N = ', num2str(N), ': ', num2str(S)]);
end
function f = fact(n)
    f = 1;
    for i = 1:n
        f = f * i;
    end
end



'''
