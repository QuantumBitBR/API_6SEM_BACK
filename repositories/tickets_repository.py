from config.db_connection import get_cursor, get_cursor_db_keys
from utils.encryptor import decrypt_data
from datetime import datetime
from typing import Optional, List, Tuple, Any, Union, Dict

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
        Ajustado para usar 'IN' para listas de IDs.
        """
        conditions = []
        params = []
        
        id_filters = {
            'companyid': company_id,
            'productid': product_id,
            'categoryid': category_id,
            'priorityid': priority_id,
        }
        
        for col_suffix, ids in id_filters.items():
            if ids is not None and ids:
                conditions.append(f"t.{col_suffix} IN %s")
                params.append(tuple(ids))
                
        if createdat is not None:
            conditions.append("t.createdat >= %s")
            params.append(createdat)
            
        if end_date is not None:
            conditions.append("t.createdat <= %s")
            params.append(end_date)

        sql_where = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        return sql_where, params
    

    def get_tickets_by_company(
        self,
        company_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        priority_id: Optional[int] = None,
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
            return cur.fetchall()
        
    def get_tickets_by_product(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por produto,
        aplicando filtros opcionais.
        """
        sql_base = """
            SELECT
                p.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                products p ON t.productid = p.productid
        """
        sql_group_by = " GROUP BY p.name;"
        
        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        
        # Concatena as partes da query
        sql_query = sql_base + sql_where + sql_group_by
        
        with get_cursor() as cur:
            cur.execute(sql_query, tuple(params))
            return cur.fetchall()

    def get_tickets_by_category(
        self,
        company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por categoria,
        aplicando filtros opcionais.
        """
        sql_base = """
            SELECT
                ca.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                categories ca ON t.categoryid = ca.categoryid
        """
        sql_group_by = " GROUP BY ca.name;"
        
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
            return cur.fetchall()

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
        aplicando filtros opcionais.
        """
        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        sql_filter_tickets = f"""
            SELECT 
                t.ticketid
            FROM 
                tickets t
            {sql_where} -- Aplicando o WHERE
        """
        
        sql_query = f"""
            WITH valid_tickets AS (
                {sql_filter_tickets}
            ),
            total_tickets AS (
                SELECT COUNT(DISTINCT tsh.ticketid) AS total_count 
        FROM 
            ticketstatushistory tsh
        JOIN 
            valid_tickets vt ON tsh.ticketid = vt.ticketid 
            )
            SELECT
                s.name,
                COALESCE(CAST(COUNT(s.name) AS REAL) * 100 / NULLIF((SELECT total_count FROM total_tickets), 0), 0) AS percentage
            FROM
                ticketstatushistory tsh
            JOIN
                statuses s ON tsh.tostatusid = s.statusid
            JOIN
                valid_tickets vt ON tsh.ticketid = vt.ticketid -- Junta apenas os tickets filtrados
            WHERE
                -- Garante que só peguemos o status mais recente dos tickets FILTRADOS
                tsh.historyid IN (
                    SELECT MAX(tsh_inner.historyid)
                    FROM ticketstatushistory tsh_inner
                    JOIN valid_tickets vt_inner ON tsh_inner.ticketid = vt_inner.ticketid -- Filtro aplicado aqui
                    GROUP BY tsh_inner.ticketid
                )
            GROUP BY
                s.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query, tuple(params))
            return cur.fetchall()
        
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
                t.device 
            FROM tickets t
            INNER JOIN companies c ON c.companyid = t.companyid
            INNER JOIN priorities prio ON prio.priorityid = t.priorityid
            INNER JOIN products p ON p.productid = t.productid
            INNER JOIN statuses s ON s.statusid = t.currentstatusid 
            INNER JOIN categories cat ON cat.categoryid = t.categoryid
            INNER JOIN subcategories s2 ON s2.subcategoryid = t.subcategoryid 
            WHERE t.ticketid = %s;
        """
        key = None
        if id:
            with get_cursor_db_keys() as cur:
                cur.execute("SELECT keyencrypt FROM encrypt_ticket WHERE ticketid = %s;", (int(id),))
                key = cur.fetchone()
                if key != None:
                    key = key[0].tobytes().decode('utf-8')

        if key != None:
            with get_cursor() as cur:
                cur.execute(sql_query, (int(id),))
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"Id {id} não encontrado!")
                            
                colnames = [desc[0] for desc in cur.description]
                row = dict(zip(colnames, list(row)))


                for k, v in row.items():
                    if isinstance(v, memoryview):
                        row[k] = v.tobytes().decode('utf-8')

                row['title'] = decrypt_data(key, row['title'])
                row['description'] = decrypt_data(key, row['description'])
                
                return row
        return False
                
    def get_by_priority(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por prioridade.
        """
        sql_base = """
            select p.name, count(p.name) as total  from tickets t
            inner join priorities p
            on t.priorityid = p.priorityid
        """

        sql_group_by = " GROUP BY p.name;"

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
            return cur.fetchall()
        
    def get_tickets_by_department(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por departamento,
        fazendo JOINs indiretos: tickets -> agents -> departments.
        Retorna uma lista de tuplas.
        """
        sql_base = """
            SELECT
                d.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                agents a ON t.assignedagentid = a.agentid
            JOIN
                departments d ON a.departmentid = d.departmentid
        """
        sql_group_by = " GROUP BY d.name;"

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
            return cur.fetchall()
        

    def get_tickets_by_slaplan(self, company_id: Optional[List[int]] = None,
        product_id: Optional[List[int]] = None,
        category_id: Optional[List[int]] = None,
        priority_id: Optional[List[int]] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        # mudar para que a porcentagem so retorne dois numeros depois da virgula
        """
        Executa a consulta no banco de dados para contar os tickets por SLAPlan.
        Retorna uma lista de tuplas (slaplan_name, ticket_count).
        """
        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        sql_base = f"""
            WITH total_tickets AS (
                SELECT COUNT(ticketid) AS total_count
                FROM tickets t
                {sql_where}
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
            {sql_where}
        """

        sql_group_by = " GROUP BY sp.name;"

        
        
        sql_query = sql_base + sql_group_by
        with get_cursor() as cur:
            cur.execute(sql_query, tuple(params*2))
            return cur.fetchall()
        
    def get_all_categories(self):
        """
        Executa a consulta no banco de dados para buscar todas as categorias de tickets.
        Retorna uma lista de tuplas (category_id, category_name).
        """
        sql_query = """
            SELECT
                categoryid,
                name
            FROM
                categories;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
        
    def get_total_ticket_count(self) -> int:
        """
        Obtém o número total de tickets na tabela 'tickets'.
        """
        count_query = "SELECT COUNT(ticketid) FROM tickets;"
        
        with get_cursor() as cur:
            cur.execute(count_query)
            total = cur.fetchone()[0] 
            
            return total
        
    def get_all_tickets_details(
        self, 
        company_id: Optional[List[int]] = None, 
        product_id: Optional[List[int]] = None, 
        category_id: Optional[List[int]] = None, 
        priority_id: Optional[List[int]] = None, 
        createdat: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        limit: int = 50
    ) -> List[Dict[str, Union[int, str]]]:
        """
        Busca todos os tickets com detalhes, aplicando filtros opcionais.
        """
        
        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        
        total_count = self.get_total_ticket_count()
        
        offset = (page - 1) * limit
        
        sql_query = """
            SELECT
                t.ticketid,
                t.title_without_encrypt as title,
                t.description_without_encrypt as description,
                c.name AS company_name,
                p.name AS product_name,
                stat.name AS status_name,
                t.channel as channel,
                t.device,
                prio.name AS priority_name,
                ca.name AS category_name,
                sub.name AS subcategory_name
            FROM 
                tickets t
            JOIN 
                companies c ON t.companyid = c.companyid
            JOIN 
                users u ON t.createdbyuserid = u.userid
            JOIN
                priorities prio ON t.priorityid = prio.priorityid
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            JOIN
                products p ON t.productid = p.productid
            JOIN
                statuses stat ON t.currentstatusid = stat.statusid
            LEFT JOIN 
                subcategories sub ON t.subcategoryid = sub.subcategoryid
            """ + sql_where + """ 
            ORDER BY t.ticketid DESC 
            LIMIT %s 
            OFFSET %s;
        """
        
        all_params = tuple(params) + (limit, offset)


        results = []
        with get_cursor() as cur:
            cur.execute(sql_query, all_params) 
            tickets_data = cur.fetchall()

            for row in tickets_data:
                results.append({
                    "ticketid": row['ticketid'],
                    "title": row['title'],
                    "description": row['description'],
                    "company_name": row['company_name'],
                    "product_name": row['product_name'],
                    "status_name": row['status_name'],
                    "channel": row['channel'],
                    "device": row['device'],
                    "priority_name": row['priority_name'],
                    "category_name": row['category_name'],
                    "subcategory_name": row['subcategory_name'] if row['subcategory_name'] else None 
                })
                
        return {
            "page": page,
            "limit": limit,
            "total_tickets": total_count,
            "total_pages": (total_count + limit - 1) // limit,
            "data": results
        }