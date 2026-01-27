# Quick Reference Guide - Django Blog Project

## 🎯 KEY CONCEPTS AT A GLANCE

### Backend Stack
- **Framework**: Django 4.2.7 (MVT Architecture)
- **Language**: Python 3.x
- **Database**: MySQL (production-ready, concurrent access)
- **ORM**: Django ORM (no raw SQL)

### Frontend Stack
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 5**: Responsive UI framework
- **JavaScript/jQuery**: Client-side interactivity
- **AJAX**: Asynchronous requests (like/dislike without reload)

---

## 📊 DATABASE MODELS

### Core Models
1. **Profile** (OneToOne with User)
2. **BlogPost** (ForeignKey to User, Category; M2M with Tag, User)
3. **Comment** (ForeignKey to Post, User; Self-referential for replies)
4. **Category** (OneToMany with BlogPost)
5. **Tag** (ManyToMany with BlogPost)
6. **Follow** (ManyToMany relationship between Users)
7. **Notification** (Tracks user notifications)

### Key Relationships
- User → Profile: OneToOne
- User → BlogPost: OneToMany (author)
- BlogPost → Category: ManyToOne
- BlogPost ↔ Tag: ManyToMany
- BlogPost ↔ User: ManyToMany (likes/dislikes)
- Comment → Comment: Self-referential (nested replies)

---

## 🔑 KEY FEATURES

### 1. User Management
- Registration, Login, Logout
- Profile creation (automatic via signals)
- Profile editing with image upload
- User following system

### 2. Content Management
- Create, Read, Update, Delete posts
- Draft system (draft/published status)
- Category and tag organization
- Rich text content

### 3. Social Features
- Like/Dislike posts and comments (AJAX)
- Nested comments (replies)
- Follow/Unfollow users
- Notifications system

### 4. Discovery
- Search functionality (title + content)
- Category filtering
- Tag-based filtering
- Popular posts section

### 5. Admin Features
- Admin dashboard
- User management
- Content moderation
- Analytics

---

## 🛡️ SECURITY FEATURES

1. **CSRF Protection**: Middleware + tokens in forms
2. **XSS Prevention**: Template auto-escaping
3. **SQL Injection**: Django ORM (parameterized queries)
4. **Authentication**: Django auth system
5. **Authorization**: @login_required, superuser checks
6. **Password Security**: PBKDF2 hashing

---

## 🔧 TECHNICAL CONCEPTS

### Django Concepts
- **MVT**: Model-View-Template architecture
- **URL Routing**: URLconf patterns
- **Middleware**: Request/response processing
- **Signals**: Event-driven programming (post_save, m2m_changed)
- **Forms**: ModelForm, Form validation
- **Pagination**: Efficient data loading
- **QuerySets**: Lazy evaluation, chaining

### Database Concepts
- **ORM Methods**: filter(), get(), exclude(), annotate()
- **Relationships**: ForeignKey, ManyToMany, OneToOne
- **Query Optimization**: select_related(), prefetch_related()
- **Aggregations**: count(), F() expressions
- **Transactions**: Atomic operations

### Frontend Concepts
- **AJAX**: Asynchronous JavaScript and XML
- **jQuery**: DOM manipulation, event handling
- **Template Inheritance**: DRY principle
- **Bootstrap**: Grid system, components

---

## 📝 COMMON INTERVIEW QUESTIONS

### Django Basics
1. **MVT vs MVC**: Explain Django's architecture
2. **ORM**: Why use ORM instead of raw SQL?
3. **QuerySets**: Lazy evaluation, when queries execute
4. **Middleware**: Order matters, what each does
5. **Signals**: When to use, decoupling benefits

### Models
6. **Relationships**: ForeignKey vs ManyToMany vs OneToOne
7. **on_delete**: CASCADE, SET_NULL, PROTECT options
8. **related_name**: Reverse relationship access
9. **Meta options**: unique_together, ordering, verbose_name

### Views
10. **FBV vs CBV**: When to use each
11. **@login_required**: How it works
12. **get_object_or_404**: Why use it
13. **Context**: How data reaches templates

### Security
14. **CSRF**: How protection works
15. **XSS**: How Django prevents it
16. **SQL Injection**: How ORM prevents it
17. **Authentication**: Session vs Token

### Performance
18. **N+1 Problem**: What it is, how to fix
19. **Query Optimization**: select_related, prefetch_related
20. **Caching**: When and how to cache

---

## 🎯 PROJECT-SPECIFIC ANSWERS

### Like/Dislike System
- Uses ManyToMany with User
- AJAX updates without page reload
- Toggle functionality (remove if exists)
- Mutual exclusion (like removes dislike)

### Nested Comments
- Self-referential ForeignKey
- Parent = None for top-level
- Recursive rendering in template
- Separate ReplyForm

### Draft System
- Status field (draft/published)
- Filter by status in queries
- DraftListView shows user drafts
- Edit to change status

### Notification System
- Signal-driven (post_save, m2m_changed)
- Auto-create on follow, comment, like
- Notification model tracks all
- is_read flag for status

### Search
- Q objects for OR conditions
- Case-insensitive (icontains)
- Search in title and content
- Optional category filter

---

## 💡 IMPROVEMENTS TO MENTION

### Performance
- Add caching (Redis)
- Optimize database queries
- Use F() expressions for counters
- Implement pagination everywhere

### Features
- REST API (DRF)
- Real-time notifications (WebSockets)
- Advanced search (Elasticsearch)
- Email notifications

### Security
- Rate limiting
- Content moderation
- Two-factor authentication
- HTTPS enforcement

### Scalability
- Database indexing
- CDN for static files
- Load balancing
- Database replication

---

## 🚀 DEPLOYMENT CHECKLIST

1. **Settings**: DEBUG=False, ALLOWED_HOSTS
2. **Database**: Production MySQL config
3. **Static Files**: Collectstatic, serve via Nginx
4. **Media Files**: Cloud storage or Nginx
5. **WSGI Server**: Gunicorn or uWSGI
6. **Web Server**: Nginx (reverse proxy)
7. **Environment Variables**: Secret key, DB credentials
8. **HTTPS**: SSL certificates
9. **Monitoring**: Error tracking, logging
10. **Backup**: Database backups

---

## 📚 KEY PYTHON/DJANGO FUNCTIONS

### QuerySet Methods
- `filter()`: Filter results
- `get()`: Get single object
- `exclude()`: Exclude results
- `order_by()`: Sort results
- `values()`: Get dicts
- `annotate()`: Add computed fields
- `aggregate()`: Aggregate functions

### Model Methods
- `save()`: Save instance
- `delete()`: Delete instance
- `__str__()`: String representation
- `get_absolute_url()`: Canonical URL

### View Helpers
- `render()`: Render template
- `redirect()`: Redirect to URL
- `get_object_or_404()`: Get or 404
- `reverse()`: Reverse URL lookup

---

## 🎓 LEARNING RESOURCES TO MENTION

- Django Official Documentation
- Django Best Practices
- Two Scoops of Django
- Real Python Django tutorials
- Django for Beginners (book)

---

**Remember**: Always explain WHY you made choices, not just WHAT you did!


