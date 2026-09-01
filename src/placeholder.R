library(dplyr)

df <- data.frame(patient_id = c("P001","P002","P003"), age = c(54, 61, 47))
print(dplyr::summarise(df, avg_age = mean(age)))

