### Database Trigger 
```
CREATE TRIGGER <TRIGGER NAME>
        AFTER UPDATE
            ON <TABLE>
BEGIN
    UPDATE <TABLE>
       SET <modified_time_column> = (datetime('now')) 
     WHERE <primary key> = new.<primary key>;
END;
```


