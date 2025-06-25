# Adding New Languages to Aufraumenbee

## Quick Reference for Adding Languages

### 1. Add to Available Languages (translations.py)
```python
'pt': {'name': 'Português', 'flag': '🇵🇹', 'locale': 'pt_PT'},
'nl': {'name': 'Nederlands', 'flag': '🇳🇱', 'locale': 'nl_NL'},
'pl': {'name': 'Polski', 'flag': '🇵🇱', 'locale': 'pl_PL'},
```

### 2. Add Translation Dictionary
Copy the English dictionary and translate all values:
```python
'pt': {
    'app_name': 'Aufraumenbee',
    'welcome': 'Bem-vindo',
    'login': 'Entrar',
    # ... all other keys
}
```

### 3. Test New Language
- Start application
- Select new language from dropdown
- Verify all text appears correctly
- Test forms and functionality

### 4. Add Database Columns (for services)
```sql
ALTER TABLE service_types ADD COLUMN name_pt TEXT;
ALTER TABLE service_types ADD COLUMN description_pt TEXT;
```

### 5. Update Service Data
```sql
UPDATE service_types SET 
name_pt = 'Limpeza Básica', 
description_pt = 'Serviço de limpeza padrão'
WHERE name_en = 'Basic Cleaning';
```

## Estimated Time per Language
- **Basic Implementation**: 2-4 hours
- **Full Translation**: 1-2 days  
- **Testing & QA**: 1 day
- **Database Updates**: 2 hours

## Priority Languages for Global Expansion
1. **Portuguese** (Brazil market)
2. **Dutch** (Netherlands market)
3. **Polish** (Poland market)
4. **Swedish** (Nordic market)
5. **Chinese** (Simplified - Asian market)
