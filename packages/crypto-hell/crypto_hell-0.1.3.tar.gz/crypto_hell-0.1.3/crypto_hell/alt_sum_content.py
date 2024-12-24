# Auto-generated file for alt_sum.m
file_content = '''
% Example usage
alternating_sum(10); % Compute the sum for N = 10
alternating_sum(20); % Compute the sum for N = 20

function S = alternating_sum(N)
    S = 0; 
    for k = 1:N
        term = (-1)^(k+1) * (2*k - 1)^2; 
        S = S + term;
    end
    disp(['Sum for N = ', num2str(N), ': ', num2str(S)]);
end

'''
