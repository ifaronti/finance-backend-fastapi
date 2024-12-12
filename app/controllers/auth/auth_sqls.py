
register_sql = f"""
        WITH is_user AS(
            INSERT INTO "user" (id, name, email, password, income, expenses, balance)
            VALUES (   
                %s,             
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            RETURNING id
        ),
        transa_insert AS(
            INSERT INTO transactions ("userId", "isPlaceholder", avatar, 
            name, amount, category, "categoryId", date, recurring)
            SELECT 
                id, data."isPlaceholder", data.avatar, data.name, data.amount,
                data.category, data."categoryId", data.date, data.recurring
            FROM is_user, json_to_recordset(%s) AS data("isPlaceholder" boolean, avatar text, 
            name text, amount decimal, category text, "categoryId" numeric, date date, recurring boolean)
        ),
        bill_insert AS(
            INSERT INTO bills ("userId", "isPlaceholder", avatar, 
                name, amount, category, "categoryId", due_day)
            SELECT 
                id, data."isPlaceholder", data.avatar, data.name, data.amount,
                data.category, data."categoryId", data.due_day
            FROM is_user, json_to_recordset(%s) AS data("isPlaceholder" boolean, avatar text, 
            name text, amount decimal, category text, "categoryId" numeric, due_day numeric)
        ),
        budgets_insert AS(    INSERT INTO budgets ("userId", "isPlaceholder", maximum, spent, category, 
                theme, "categoryId")
            SELECT
                id, data."isPlaceholder", data.maximum, data.spent, data.category,
                data.theme, data."categoryId"
            FROM is_user, json_to_recordset(%s) AS data("isPlaceholder" boolean, maximum decimal, 
            spent decimal, category text, theme text, "categoryId" numeric)
        ),
        pots_insert AS(
            INSERT INTO pots ("userId", "isPlaceholder", name, target, total, theme)
            SELECT
                id, data."isPlaceholder", data.name, data.target, data.total, data.theme
            FROM
                is_user, json_to_recordset(%s) AS data("isPlaceholder" boolean, name text, 
                target decimal, total decimal, theme text)
        )
    SELECT id FROM is_user
    """