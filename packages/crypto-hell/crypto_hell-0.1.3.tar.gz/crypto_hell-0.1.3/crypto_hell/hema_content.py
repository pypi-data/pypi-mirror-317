# Auto-generated file for hema.m
file_content = '''
clc;
clear all;
disp("=========== Enter matrix one informations ===========");
[noRowsMat_one, noColsMat_one] = getMatrixInformations();
matrix_one = readMatrixItems(noRowsMat_one, noColsMat_one);
disp("=========== Enter matrix two informations ===========");
[noRowsMat_two, noColsMat_two] = getMatrixInformations();
matrix_two = readMatrixItems(noRowsMat_two, noColsMat_two);
if noColsMat_one == noRowsMat_two
    result = multiplicationMatrix(matrix_one, noRowsMat_one, noColsMat_one, matrix_two, noColsMat_two);
    disp("Result of multiplication:");
    disp(matrix_one);
    disp('*');
    disp(matrix_two);
    disp('_');
    disp(result);
else
    disp("Matrices can't be multiplied");
end

function [noRows, noCols] = getMatrixInformations
    noRows = input("Enter number of rows: ");
    noCols = input("Enter number of columns: ");
end

function matrix = readMatrixItems(noRows, noCols)
    matrix = zeros(noRows, noCols);
    for i = 1:noRows
        for j = 1:noCols
            caption = sprintf('Enter value of position [%d][%d]: ', i, j);
            matrix(i, j) = input(caption);
        end
    end
end

function multiplicationResultMatrices = multiplicationMatrix(matrixOne, noRowsMatOne, noColsMatOne, matrixTwo, noColsMatTwo)
    multiplicationResultMatrices = zeros(noRowsMatOne, noColsMatTwo);
    for i = 1:noRowsMatOne
        for j = 1:noColsMatTwo
            for k = 1:noColsMatOne
                multiplicationResultMatrices(i, j) = multiplicationResultMatrices(i, j) + matrixOne(i, k) * matrixTwo(k, j);
            end
        end
    end
end
'''
