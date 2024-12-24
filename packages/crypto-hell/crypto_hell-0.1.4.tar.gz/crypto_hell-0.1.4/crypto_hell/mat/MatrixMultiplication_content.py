# Auto-generated file for MatrixMultiplication.m
file_content = '''

A = [1, 3, -1; 1, 0, -1; 0, 4, 2];
B = [-1, 0; 2, 1; 4, 2];

C = matmul(A, B);
disp('Resultant Matrix C:');
disp(C);

function C = matmul(A, B)
    [rowsA, colsA] = size(A);
    [rowsB, colsB] = size(B);

    C = zeros(rowsA, colsB);

    if colsA ~= rowsB
        error('Matrix dimensions do not match for multiplication');
    end

    for i = 1:rowsA
        for j = 1:colsB
            for k = 1:colsA
                C(i, j) = C(i, j) + A(i, k) * B(k, j);
            end
        end
    end
end


'''
