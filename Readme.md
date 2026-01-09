# OBT (OurBugTracker)  Backend

OBT is a fullstack bug tracking platform useful to for dev teams and reporters to manage bugs on multiple projects. This is the backend infrastructure, feel free to use for your course, the frontend will soon be available for display and both ends will be improved overtime.



---


## 🛠 Backend Features

### ✅ Completed

* [x] User registration, authentication, and role management (`CustomUser`)
* [x] CRUD operations for **Issues / Bugs**

  * [x] Create, read, update, delete issues
  * [x] Issue filtering by project, status, priority, assignee
  * [x] Permissions: Only admin or project members can create/edit issues
  * [x] Include related comments in issue serializer
* [x] CRUD operations for **Comments**

  * [x] Only issue creator, assignee, or admin can comment
  * [x] Validation for issue commenting permissions
* [x] Projects CRUD

  * [x] Project creation, read, update
  * [x] Serializer returns members
  * [x] Permissions: Only creator or admin can edit project
* [x] Audit logs for issue actions (read-only serializer)
* [x] Permissions enforced using DRF `permission_classes`
* [x] API endpoints:

  * `/projects/`
  * `/projects/<id>/`
  * `/issues/`
  * `/issues/<id>/`
  * `/comments/`

---

### 🔜 To Implement / Remaining

* [ ] **Project Membership System**

  * [ ] Support multiple members per project
  * [ ] Endpoint to add/remove members (only creator/admin)
  * [ ] Ensure only members can create/edit issues in a project
* [ ] **Project Role-based Access**

  * [ ] Creator and admin can edit project
  * [ ] Staff permission check for adding members
* [ ] **User Projects Endpoint**

  * [ ] List all projects a user is a member of
  * [ ] Optional: Include counts of issues (open/closed)
* [ ] **Audit Log Improvements**

  * [ ] Track project changes
  * [ ] Include member additions/removals
* [ ] **Notifications / Email Alerts**

  * [ ] On new issue creation
  * [ ] On comments for issues
* [ ] **Optional Security Enhancements**

  * [ ] Rate limiting on endpoints
  * [ ] Input sanitization and validation improvements

---

## 💻 Frontend Features

### ✅ Completed

* [x] **Dashboard Pages**

  * [x] Project page: List project details, members, and issues
  * [x] Bug detail page: Show issue, comments, status update dropdown
* [x] **Forms**

  * [x] BugForm – create/edit bug
  * [x] ProjectForm – create/edit project
  * [x] AddCommentForm – add comments to issues
* [x] **UI Feedback**

  * [x] Loading states
  * [x] Disabled buttons during submission
  * [x] Conditional rendering for user permissions
* [x] API integration for:

  * Projects (`getProjectDetails`, `updateProject`, `getProjects`)
  * Issues (`getAllBugs`, `createBug`, `updateBug`, `getIssuesByProject`)
  * Comments (`createComment`, `getComments`)
* [x] Conditional UI rendering

  * [x] Show/hide “Add Issue” or “Edit Project” buttons based on user role or membership
  * [x] Comments restricted to members

---

### 🔜 To Implement / Remaining

* [ ] **Project Member Management UI**

  * [ ] Add/remove members (frontend component)
  * [ ] Show roles of members
* [ ] **User Projects Page**

  * [ ] List all projects a user belongs to
  * [ ] Link to project details
* [ ] **Enhanced Notifications / Feedback**

  * [ ] Toast messages for API success/failure
  * [ ] Optimistic UI updates for comments/issues/projects
* [ ] **UI Polishing**

  * [ ] Better loading skeletons
  * [ ] Mobile/responsive improvements
* [ ] **Search / Filter Enhancements**

  * [ ] Filter issues by status, priority, assignee on frontend
* [ ] **Deployment Optimizations**

  * [ ] Environment variables for API URLs
  * [ ] Error boundary for network failures

---

### 🔮 Future / Nice-to-Have

* [ ] Real-time updates via WebSockets or Pusher
* [ ] Tagging system for issues
* [ ] Analytics: Open/Closed issues per project
* [ ] Dark mode toggle
* [ ] User settings/profile page
* [ ] Multi-language support

---

