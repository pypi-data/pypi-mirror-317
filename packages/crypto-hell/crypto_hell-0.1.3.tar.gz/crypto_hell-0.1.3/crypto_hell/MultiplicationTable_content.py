# Auto-generated file for MultiplicationTable.m
file_content = '''
% Example usage
multiplication_table(7);

function multiplication_table(n)
    % Generate and display the multiplication table
    for i = 1:n
        for j = 1:n
            fprintf('%d x %d = %d\n', i, j, i * j);
        end
        fprintf('\n'); % Add a blank line after each row
    end
end


'''
