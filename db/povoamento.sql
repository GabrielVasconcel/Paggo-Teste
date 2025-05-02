DO $$
DECLARE
-- Periodo de 10 dias, com intervalos de 1 minuto
    inicio TIMESTAMP := '2025-01-01 00:00:00';
    fim TIMESTAMP := '2025-01-11 00:00:00';
BEGIN
    WHILE inicio < fim LOOP
        INSERT INTO data (timestamp, wind_speed, power, ambient_temperature)
        VALUES (
            inicio,
            random() * 15,                          
            random() * 500 + 100,                   
            random() * 15 + 15                       
        );
        inicio := inicio + interval '1 minute';
    END LOOP;
END $$;
