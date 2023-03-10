# Предварительный анализ задачи определения мошеннических финансовых операций

## 1. Цели проектируемой системы
 - Оценка в реальном времени на основе машинного обучения проводимого
онлайн-платежа на предмет, является ли он мошенническим
 - Обеспечить пропускную способность 50 RPS 97% времени и в оставшееся время - 
до 500 RPS.
 - Обеспечить пропуск мошеннических платежей на уровне не выше 2% от всех платежей
 - Обеспечить классификацию корректных транзакций как мошеннические на уровне не 
выше 5% от всех платежей
 - Обеспечить суммарные потери клиентов на уровне не выше x руб/мес
 - Система должна функционировать в облаке с доступом для внешнего использования

## 2. Метрики качества системы
Для оценки использовать метрики качества бинарной классификации мошенник / не мошенник:
 - **Precision** - не ниже 90%. Доля ложных среди всех срабатываний равняется 10%, 
а среди всех кейсов будет стремиться от 5% к 0% (при переходе от сбалансированного
датасета до реалистичного с преобладанием нормальных транзакций).
 - **Recall** - не ниже 96%. Доля ложных пропусков среди всех мошеннических платежей
равняется 4%, а среди всех кейсов будет стремиться от 2% до 0% (при переходе от
сбалансированного датасета до реалистичного с преобладанием нормальных транзакций).


## 3. Особенности проекта
### Money
* Бюджет проекта - 10млн рублей без учёта зп сотрудников
* Заказчик не предоставляет свои вычислительные мощности, поэтому часть бюджета 
пойдёт на инфраструктуру
* MVP проект займёт 3 месяца, после чего будет принято решение о 
целесообразности продолжения
* В случае положительного решения завершить проект нужно за 6 месяцев. Таким
образом, бюджет в 10млн рублей предполагается освоить за 9 месяцев
* Денежная цель проекта - уменьшить ущерб клиента от мошенников. Целевой
ориентир - это конкурент, убытки клиентов которого составляют не более 500
тыс. руб. на всех клиентов в месяц
### Ideas
* Гипотеза - модель, основанная на машинном обучении, будет автоматически
классифицировать транзакцию на мошенническую/нормальную и отклонять в первом
случае. Такой подход позволит уменьшить долю мошеннических операций до 2%
и уменьшить ущерб клиента до целевого 

* До 80% Precision и 80% Recall можно получить с помощью одних лишь существующих
моделей

### Strategy
* Хозяин бюджета - руководство компании
* Стратегические цели - улучшение качества сервиса платежей и сохранение лояльности
клиентов
* Руководство заинтересовано в проекте, но может закрыть его в случае
неудовлетворительного MVP

### Skills
Требуемые компетенции:
* Product owner +
* Менеджер проекта +
* Senior data-scientist + (не первая антифрод система в компании, работал на двух 
аналогичных проектах)
* Junior/middle data-scientists (1-2 человека) +
* Эксперт домена + (аналитики платежной системы доступны, т.к. это внутренняя 
разработка)
* Инженер нагруженных систем + (компания регулярно сталкивается с подобными запросами)
### Inputs
* Источник данных для обучения - исторические данные платёжной системы
* Данные внутри самой компании, процесс согласования и передачи не должен быть проблемным
* Формат данных csv
* Данные персонифицированы, для максимальной безопасности их нужно деперсонифицровать
перед обучением
* Количество данных для обучения будут определять ресёрчеры в процессе технической
проработки
### Outputs
ML решение, требуемое на выходе описано в п. Цели проектируемой системы

### Nuances
Недопустима утечка данных клиентов, это большой репутационный риск

## 4. Декомпозиция системы
Высокоуровнево сервис классификации транзакций состоит из следующих частей:
* REST-сервис - API для работы с антифрод-классификатором.
* Антифрод-классификатор – сервис с моделью для обнаружения мошеннических платежей
* Лог транзакций – NoSQL хранилище информации о транзакциях.

## 5. Задачи для реализации системы
Для наглядности задачи для реализации сгруппированы в дерево. Родительские задачи
перечисляются через слеш. Длительность для краткости обозначена в скобках.
* **Утвердить требования к MVP (5д)**. В течение первой недели проекта 
  согласовать требования к MVP версии системы, которую нужно реализовать за три
  месяца. Требования зафиксировать в документе _url_
* **Данные**
  * **Данные / Клиентские**
    * **Данные / Клиентские / Утвердить требования к данным (2ч)** Провести интервью с
    дата-сайентистами и определить требования к данным от клиента (количество, 
    период, т.д.). Результаты зафиксировать в документе - _url_
    * **Данные / Клиентские / Получить данные от клиента (1д)**. Представитель клиента
    И. Иванов (контактные данные). Связаться и обсудить деперсонификацию данных
    (на стороне клиента) и выгрузку в соответствии с требованиями дата-сайентистов _url_.
    Данные от клиента положить в хранилище - _url_
  * **Данные / Открытый доступ**
    * **Данные / Открытый доступ / Поиск бесплатных датасетов (1д)** Найти размеченные 
    данные по теме мошеннических платежей. Составить сводную таблицу всех 
    датасетов _url_
    * **Данные / Открытый доступ / Выгрузка найденных датасетов (3ч)** Выгрузить бесплатные
    датасеты в хранилище - _url_
* **Модель**
  * **Модель / Baseline (4ч)** Разработать дамми-модель для бинарной классификации
  * **Модель / Разработка (NA)** Разработать модель в соответствии с утверждёнными
  требованиями к качеству MVP - _url_. *_Задача для дальнейшего дробления_
* **Модуль**
  * **Модуль / Архитектура (3д)** Разработать архитектуру решения в формате UML
  в соответствии с утверждёнными требованиями к MVP - _url_
  * **Модуль / Реализация (NA)** Разработать модуль в соответствии с утверждёнными
  требованиями к MVP - _url_. *_Задача для дальнейшего дробления_
  * **Модуль / Встраивание модели в приложение (3д)** Встроить обученную модель
  в облачное приложение
## 6. Kanban доска
[https://github.com/users/inna-tuzhikova/projects/2](https://github.com/users/inna-tuzhikova/projects/2)
