-- ============================================
-- Inicialización de la base de datos
-- Este script se ejecuta automáticamente
-- la primera vez que arranca el contenedor.
-- ============================================

CREATE TABLE IF NOT EXISTS contacts (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(120) NOT NULL,
    phone VARCHAR(30)  NOT NULL,
    email VARCHAR(120)
);

-- Datos de ejemplo (opcional)
INSERT INTO contacts (name, phone, email) VALUES
    ('Juan Pérez',   '612345678', 'juan@example.com'),
    ('María García',  '698765432', 'maria@example.com'),
    ('Carlos López',  '655112233', 'carlos@example.com');
