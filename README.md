visualization:
- http://www.cp-ville.com/cpcom.php?cpcommune=paris
- http://leafletjs.com/
- http://leafletjs.com/examples/choropleth.html
- http://bl.ocks.org/pere/3012590

- http://newcoder.io/Part-4-Pipelining-data/

SET client_encoding = 'UTF8';
psql -h localhost -d myapp -U myapp

==> default: Your PostgreSQL database has been setup and can be accessed on your local machine on the forwarded port (default: 15432)
==> default:   Host: localhost
==> default:   Port: 15432
==> default:   Database: myapp
==> default:   Username: myapp
==> default:   Password: dbpass
==> default:
==> default: Admin access to postgres user via VM:
==> default:   vagrant ssh
==> default:   sudo su - postgres
==> default:
==> default: psql access to app database user via VM:
==> default:   vagrant ssh
==> default:   sudo su - postgres
==> default:   PGUSER=myapp PGPASSWORD=dbpass psql -h localhost myapp
==> default:
==> default: Env variable for application development:
==> default:   DATABASE_URL=postgresql://myapp:dbpass@localhost:15432/myapp
==> default:
==> default: Local command to access the database via psql:
==> default:   PGUSER=myapp PGPASSWORD=dbpass psql -h localhost -p 15432 myapp
