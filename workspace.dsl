workspace {

    model {
        user1 = person "Отправитель" "Отправляет посылки"
        
        user2 = person "Получатель" "Получает посылки"
        
        system = softwareSystem "Сервис доставки посылок" {
            description "Управляет аккаунтами пользователей, посылками и доставками"
        
            website = container "Веб-сайт" {
                description "Предоставляет графический интерфейс, взаимодействует с пользователями и сервисами"
                technology "HTML, CSS, JavaScript"
            }
            
            parcel = container "Посылка"
            
            delivery = container "Доставка"
            
            userAccount = container "Аккаунт пользователя"
            
            parcelService = container "Сервис посылок" {
                description "Осуществляет управление посылками"
                technology "FastAPI
                website -> this "Отправляет запросы и получает ответы" "Fetch API, JSON, HTTP"
                this -> parcel
            }
            
            deliveryService = container "Сервис доставок" {
                description "Осуществляет управление доставками"
                technology "FastAPI
                website -> this "Отправляет запросы и получает ответы" "Fetch API, JSON, HTTP"
                this -> delivery
            }
            
            userAccountService = container "Сервис аккаунтов пользователей" {
                description "Осуществляет управление аккаунтами пользователей"
                technology "FastAPI"
                website -> this "Отправляет запросы и получает ответы" "Fetch API, JSON, HTTP"
                this -> userAccount
            }
            
            dbms = container "СУБД" {
                description "Хранит данные о сущностях в таблицах и управляет ими"
                technology "PostgreSQL"
                parcel -> this "Отправляются в и загружаются из" "SQLAlchemy"
                delivery -> this "Отправляются в и загружаются из" "SQLAlchemy"
                userAccount -> this "Отправляются в и загружаются из" "SQLAlchemy"
            }
        }

        user1 -> website "Создаёт аккаунт, создаёт посылку, получает список посылок..." "Браузер"
        user2 -> website "Создаёт аккаунт, получает информацию о доставке..." "Браузер"
        
    }

    views {
        themes default
        
        systemContext system {
            include *
            autoLayout lr
        }
        
        container system {
            include *
            autolayout lr
        }
        
        dynamic system "createUser" {
            description "Создание аккаунта пользователя"
            autolayout lr
            
            user1 -> website "Создаёт аккаунт"
            website -> userAccountService "POST /users"
            userAccountService -> userAccount "Проверяет, нет ли уже аккаунта с таким логином, хэширует пароль"
            userAccount -> dbms "INSERT INTO users \n VALUES (?, ?, ?)"
        }
    }
    
}