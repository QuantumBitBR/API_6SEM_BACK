from config.db_connection import get_cursor
from utils.encryptor import decrypt_data
from datetime import datetime
from typing import Optional, List, Tuple, Any, Union, Dict
from decimal import Decimal

class TicketsRepository:

    def _build_where_clause_and_params(
        self,
        company_id: Optional[List[int]] = None, 
        product_id: Optional[List[int]] = None, 
        category_id: Optional[List[int]] = None, 
        priority_id: Optional[List[int]] = None, 
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[str, List[Any]]:
        """
        Constrói a cláusula WHERE e a lista de parâmetros para a consulta SQL.
        """
        conditions = []
        params = []
        
    
        if company_id is not None and company_id:
            conditions.append("t.companyid IN %s")
            params.append(tuple(company_id))
            
        if product_id is not None and product_id:
            conditions.append("t.productid IN %s")
            params.append(tuple(product_id))
            
        if category_id is not None and category_id:
            conditions.append("t.categoryid IN %s")
            params.append(tuple(category_id))
            
        if priority_id is not None and priority_id:
            conditions.append("t.priorityid IN %s")
            params.append(tuple(priority_id))
                
        # Filtros de data
        if createdat is not None:
            conditions.append("t.createdat >= %s")
            params.append(createdat)
            
        if end_date is not None:
            conditions.append("t.createdat <= %s")
            params.append(end_date)

        sql_where = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        return sql_where, params

    def _convert_decimals(self, data):
        """Converte objetos Decimal para float para serialização JSON."""
        if isinstance(data, Decimal):
            return float(data)
        elif isinstance(data, dict):
            return {k: self._convert_decimals(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_decimals(item) for item in data]
        elif isinstance(data, tuple):
            return tuple(self._convert_decimals(item) for item in data)
        else:
            return data

    def _process_query_result(self, results):
        """Processa os resultados da query convertendo Decimals para float."""
        processed_results = []
        for row in results:
            if isinstance(row, tuple):
                processed_row = tuple(self._convert_decimals(item) for item in row)
                processed_results.append(processed_row)
            else:
                processed_results.append(self._convert_decimals(row))
        return processed_results
    

    def get_tickets_by_company(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por empresa,
        aplicando filtros opcionais.
        """
        sql_base = """
            SELECT 
                c.name,
                COUNT(t.ticketid) AS ticket_count
            FROM 
                tickets t
            JOIN 
                companies c ON t.companyid = c.companyid
            JOIN
                products p ON t.productid = p.productid
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            JOIN
                priorities prio ON t.priorityid = prio.priorityid
        """
        sql_group_by = " GROUP BY c.name;"

        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        
        sql_query = sql_base + sql_where + sql_group_by
        
        with get_cursor() as cur:
            cur.execute(sql_query, tuple(params))
            results = cur.fetchall()
            return self._process_query_result(results)
        
    def get_tickets_by_product(self):
        """
        Executa a consulta no banco de dados para contar os tickets por produto.
        """
        sql_query = """
            SELECT
                p.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                products p ON t.productid = p.productid
            GROUP BY
                p.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            return self._process_query_result(results)

    def get_tickets_by_category(self):
        """
        Executa a consulta no banco de dados para contar os tickets por categoria.
        """
        sql_query = """
            SELECT
                ca.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            GROUP BY
                ca.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            return self._process_query_result(results)

    def get_tickets_by_status(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por status,
        aplicando filtros opcionais. Retorna apenas status_name e percentage.
        """
       
        sql_total = """
            SELECT COUNT(t_total.ticketid) AS total_count
            FROM tickets t_total
            JOIN companies c_total ON t_total.companyid = c_total.companyid
            JOIN products p_total ON t_total.productid = p_total.productid
            JOIN categories ca_total ON t_total.categoryid = ca_total.categoryid
            JOIN priorities prio_total ON t_total.priorityid = prio_total.priorityid
        """
        
        
        conditions_total = []
        params_total = []
        
       
        if company_id is not None and company_id:
            conditions_total.append("t_total.companyid IN %s")
            params_total.append(tuple(company_id))
            
        if product_id is not None and product_id:
            conditions_total.append("t_total.productid IN %s")
            params_total.append(tuple(product_id))
            
        if category_id is not None and category_id:
            conditions_total.append("t_total.categoryid IN %s")
            params_total.append(tuple(category_id))
            
        if priority_id is not None and priority_id:
            conditions_total.append("t_total.priorityid IN %s")
            params_total.append(tuple(priority_id))
                
       
        if createdat is not None:
            conditions_total.append("t_total.createdat >= %s")
            params_total.append(createdat)
            
        if end_date is not None:
            conditions_total.append("t_total.createdat <= %s")
            params_total.append(end_date)

        sql_where_total = " WHERE " + " AND ".join(conditions_total) if conditions_total else ""
        sql_total += sql_where_total
        
       
        sql_main = """
            SELECT 
                s.name as status_name,
                ROUND(
                    COUNT(t.ticketid) * 100.0 / (
        """
        sql_main += sql_total  
        sql_main += """
                    ), 2
                ) as percentage
            FROM tickets t
            JOIN statuses s ON t.currentstatusid = s.statusid
            JOIN companies c ON t.companyid = c.companyid
            JOIN products p ON t.productid = p.productid
            JOIN categories ca ON t.categoryid = ca.categoryid
            JOIN priorities prio ON t.priorityid = prio.priorityid
        """
        
        
        conditions_main = []
        params_main = []
        
       
        if company_id is not None and company_id:
            conditions_main.append("t.companyid IN %s")
            params_main.append(tuple(company_id))
            
        if product_id is not None and product_id:
            conditions_main.append("t.productid IN %s")
            params_main.append(tuple(product_id))
            
        if category_id is not None and category_id:
            conditions_main.append("t.categoryid IN %s")
            params_main.append(tuple(category_id))
            
        if priority_id is not None and priority_id:
            conditions_main.append("t.priorityid IN %s")
            params_main.append(tuple(priority_id))
                
        
        if createdat is not None:
            conditions_main.append("t.createdat >= %s")
            params_main.append(createdat)
            
        if end_date is not None:
            conditions_main.append("t.createdat <= %s")
            params_main.append(end_date)

        sql_where_main = " WHERE " + " AND ".join(conditions_main) if conditions_main else ""
        
        sql_query = sql_main + sql_where_main + " GROUP BY s.name ORDER BY percentage DESC;"
        
        # Combina os parâmetros
        all_params = params_total + params_main
        
       
        with get_cursor() as cur:
            cur.execute(sql_query, tuple(all_params))
            results = cur.fetchall()
            return self._process_query_result(results)
        
    def get_by_id(self, id: int):
        sql_query = """
            SELECT 
                t.ticketid,
                t.description, 
                t.title, 
                c.name AS company_name, 
                p.name AS product_name, 
                cat.name AS category_name, 
                s2.name AS subcategory_name,
                prio.name AS priority_name, 
                s.name AS status_name, 
                t.channel, 
                t.device, 
                e.keyencrypt
            FROM tickets t
            INNER JOIN companies c ON c.companyid = t.companyid
            INNER JOIN priorities prio ON prio.priorityid = t.priorityid
            INNER JOIN products p ON p.productid = t.productid
            INNER JOIN statuses s ON s.statusid = t.currentstatusid 
            INNER JOIN categories cat ON cat.categoryid = t.categoryid
            INNER JOIN subcategories s2 ON s2.subcategoryid = t.subcategoryid 
            INNER JOIN encrypt_ticket e ON e.ticketid = t.ticketid
            WHERE t.ticketid = %s;
        """

        with get_cursor() as cur:
            cur.execute(sql_query, (int(id),))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Id {id} não encontrado!")

            if isinstance(row, tuple):
                colnames = [desc[0] for desc in cur.description]
                row = dict(zip(colnames, row))

            for k, v in row.items():
                if isinstance(v, memoryview):
                    row[k] = v.tobytes().decode('utf-8')

            key = row['keyencrypt']
            row['title'] = decrypt_data(key, row['title'])
            row['description'] = decrypt_data(key, row['description'])

            row.pop('keyencrypt', None)

            return self._convert_decimals(row)
                
    def get_by_priority(self):
        """
        Executa a consulta no banco de dados para contar os tickets por prioridade.
        """
        sql_query = """
            select p.name, count(p.name) as total  from tickets t
            inner join priorities p
            on t.priorityid = p.priorityid
            group by p.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            return self._process_query_result(results)
        
    def get_tickets_by_department(self):
        """
        Executa a consulta no banco de dados para contar os tickets por departamento,
        fazendo JOINs indiretos: tickets -> agents -> departments.
        Retorna uma lista de tuplas.
        """
        sql_query = """
            SELECT
                d.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                agents a ON t.assignedagentid = a.agentid
            JOIN
                departments d ON a.departmentid = d.departmentid
            GROUP BY
                d.name;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            return self._process_query_result(results)
        
    def get_tickets_by_slaplan(self):
        """
        Executa a consulta no banco de dados para contar os tickets por SLAPlan.
        Retorna uma lista de tuplas (slaplan_name, ticket_count).
        """
        sql_query = """
            WITH total_tickets AS (
                SELECT COUNT(ticketid) AS total_count
                FROM tickets
                WHERE slaplanid IS NOT NULL
            )
            SELECT
                sp.name,
                CAST(
                    ROUND(
                        CAST(COUNT(sp.name) AS NUMERIC) * 100 / (SELECT total_count FROM total_tickets),
                        2
                    ) AS DOUBLE PRECISION
                ) AS percentage
            FROM
                tickets t
            JOIN
                sla_plans sp ON t.slaplanid = sp.slaplanid
            GROUP BY
                sp.name;
        """
        with get_cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall()
            return self._process_query_result(results)