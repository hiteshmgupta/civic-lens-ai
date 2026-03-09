package com.civiclens.analytics;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class ControversyEvaluator {

    // Set this to the maximum expected comments in your dataset/system
    private static final int MAX_COMMENT_COUNT = 1000;
    
    public static void main(String[] args) {
        // Paths for input and output
        String excelFilePath = "controversy_test_data_1000.xlsx";
        String csvOutputPath = "evaluation_results.csv";

        ControversyCalculator calculator = new ControversyCalculator();

        int totalSamples = 0;
        int correctPredictions = 0;

        try (FileInputStream fis = new FileInputStream(new File(excelFilePath));
             Workbook workbook = new XSSFWorkbook(fis);
             FileWriter csvWriter = new FileWriter(csvOutputPath)) {

            Sheet sheet = workbook.getSheetAt(0);
            
            // Map to store column indices dynamically
            Map<String, Integer> headerMap = new HashMap<>();
            Row headerRow = sheet.getRow(0);
            
            for (Cell cell : headerRow) {
                headerMap.put(cell.getStringCellValue().trim(), cell.getColumnIndex());
            }

            // Write CSV Header
            csvWriter.append("amendment_id,expected_controversy,predicted_controversy,controversy_score\n");

            System.out.println("Starting Evaluation...\n");
            System.out.printf("%-15s %-20s %-20s %-10s%n", "Amendment ID", "Expected", "Predicted", "Score");
            System.out.println("----------------------------------------------------------------------");

            // Iterate through rows (skipping header)
            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                // 1. Extract Data
                String amendmentId = getCellStringValue(row.getCell(headerMap.get("amendment_id")));
                int upvotes = (int) row.getCell(headerMap.get("upvotes")).getNumericCellValue();
                int downvotes = (int) row.getCell(headerMap.get("downvotes")).getNumericCellValue();
                double sentimentVariance = row.getCell(headerMap.get("sentiment_variance")).getNumericCellValue();
                int commentCount = (int) row.getCell(headerMap.get("comment_count")).getNumericCellValue();
                
                int supportCount = (int) row.getCell(headerMap.get("support_count")).getNumericCellValue();
                int opposeCount = (int) row.getCell(headerMap.get("oppose_count")).getNumericCellValue();
                int neutralCount = (int) row.getCell(headerMap.get("neutral_count")).getNumericCellValue();
                int suggestionCount = (int) row.getCell(headerMap.get("suggestion_count")).getNumericCellValue();
                
                String expectedControversy = row.getCell(headerMap.get("expected_controversy")).getStringCellValue().trim();

                // 2. Build Stance Map
                Map<String, Integer> stanceCounts = new HashMap<>();
                stanceCounts.put("Support", supportCount);
                stanceCounts.put("Oppose", opposeCount);
                stanceCounts.put("Neutral", neutralCount);
                stanceCounts.put("Suggestion", suggestionCount);

                // 3. Calculate Components
                double P = calculator.votePolarity(upvotes, downvotes);
                double S = sentimentVariance;
                double D = calculator.stanceEntropy(stanceCounts);
                double E = calculator.engagementIntensity(commentCount, MAX_COMMENT_COUNT);

                // 4. Compute Final Score & Label
                double finalScore = calculator.controversyScore(S, P, D, E);
                String predictedControversy = calculator.controversyLabel(finalScore);

                // 5. Check Accuracy
                totalSamples++;
                boolean isCorrect = expectedControversy.equalsIgnoreCase(predictedControversy);
                if (isCorrect) {
                    correctPredictions++;
                }

                // 6. Print to Console
                System.out.printf("%-15s %-20s %-20s %.4f%n", 
                        amendmentId, expectedControversy, predictedControversy, finalScore);

                // 7. Write to CSV
                csvWriter.append(String.format("%s,%s,%s,%.4f\n", 
                        amendmentId, expectedControversy, predictedControversy, finalScore));
            }

            // 8. Print Final Statistics
            double accuracy = ((double) correctPredictions / totalSamples) * 100;
            
            System.out.println("\n==================================");
            System.out.println("       EVALUATION RESULTS         ");
            System.out.println("==================================");
            System.out.println("Total Samples       : " + totalSamples);
            System.out.println("Correct Predictions : " + correctPredictions);
            System.out.printf("Accuracy Percentage : %.2f%%%n", accuracy);
            System.out.println("Results exported to : " + csvOutputPath);

        } catch (IOException e) {
            System.err.println("Error reading the Excel file or writing the CSV: " + e.getMessage());
        }
    }

    // Helper method to handle ID column being parsed as numeric or string
    private static String getCellStringValue(Cell cell) {
        if (cell.getCellType() == CellType.NUMERIC) {
            return String.valueOf((int) cell.getNumericCellValue());
        }
        return cell.getStringCellValue();
    }
}