# Auto-generated file for Compute3Tn.m
file_content = '''
% Example usage
n_values = [10, 20, 30, 50]; 
for n = n_values
    disp(['T(', num2str(n), ') = ', num2str(compute_T(n))]);
end

function T = compute_T(n)
    if n == 0
        T = 1;
    else
        T = 3 * compute_T(n - 1);
    end
end


'''
