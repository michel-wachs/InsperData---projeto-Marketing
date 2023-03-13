library(readxl)
library(dplyr)

base <- read_excel("Michel/Insper/Entidades/Insper Data/Marketing 2022.1/Base_selenium3.xlsx", 
                 col_types = c("skip", "text", "numeric", 
                               "numeric", "numeric"))
View(base)

base2 <- base %>% 
          group_by(Nome, Volume, Score) %>% 
          summarise(Preço = mean(Preço))

View(base2)

aval <- read_excel("Michel/Insper/Entidades/Insper Data/Marketing 2022.1/Aval_selenium_com_dados (1).xlsx",
                   col_types = c("skip", "skip", "text", "text", "numeric", "skip", "skip", "text", 
                                 "numeric", "numeric", "numeric", "numeric", "numeric", "numeric",
                                 "numeric", "numeric"))
View(aval)


final <- full_join(aval, base2, by = "Nome")
View(final)

final <- final[-duplicated(final), ]
final["Sentimento"] <- as.factor(ifelse(final$Positivo > final$Negativo, 1, 0)) 


library(randomForest)
idx <- sample(1:nrow(final), size = round(0.7 * nrow(final)))
training <- final[idx, ]
test <- final[-idx, ]

rf <- randomForest(Volume ~ ., data = training)
y_hat_rf <- predict(rf, data = test) 
(rmse_rf <- sqrt(mean((y_hat_rf - test$Volume)^2)))


varImpPlot(rf, bg = "red", main = "Nível de importância de cada variável")

library(ggplot2)


ggplot(final, aes(x = Preço, y = Volume, col = Score)) +
  geom_point() + 
  scale_color_gradient(low = "blue", high = "red") +
  facet_wrap(~maior_classe)

final %>% 
  group_by(Nome, Volume, Score) %>% 
  summarise(Sentimento = mean(Sentimento)) %>% 
  ggplot(aes(x = reorder(Nome, -Sentimento), y = Sentimento, col = Score)) +
    geom_point()+
    scale_color_gradient(low = "blue", high = "red") +
    theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())

final %>% 
  group_by(Nome, Volume, Score) %>% 
  summarise(Sentimento = mean(Sentimento)) %>% 
  ggplot(aes(x = reorder(Nome, -Sentimento), y = Sentimento, col = Volume)) +
  geom_point()+
  scale_color_gradient(low = "blue", high = "red") +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())


ggplot(final, aes(x = as.factor(maior_classe), y = Volume, 
                  fill = as.factor(maior_classe))) +
  geom_boxplot() +
  facet_wrap(~as.factor(Sentimento)) +
  theme(axis.title.x=element_blank()) + 
  theme(legend.position = "none")




