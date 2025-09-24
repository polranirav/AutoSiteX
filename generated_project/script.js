class TodoApp {
    constructor() {
        this.tasks = [];
        this.currentId = 0;
        this.init();
    }

    init() {
        // Add event listeners for user input
        document.getElementById('addTaskBtn').addEventListener('click', () => this.handleAddTask());
        document.getElementById('taskList').addEventListener('click', (e) => this.handleTaskClick(e));
        document.getElementById('themeSwitcher').addEventListener('click', () => this.changeTheme());
    }

    handleAddTask() {
        const taskInput = document.getElementById('taskInput');
        const taskContent = taskInput.value.trim();
        if (taskContent) {
            this.addTask(taskContent);
            taskInput.value = '';
        }
    }

    handleTaskClick(event) {
        const target = event.target;
        const taskId = target.dataset.id;
        if (target.classList.contains('edit-btn')) {
            const newTaskContent = prompt('Edit task:', this.tasks[taskId].content);
            if (newTaskContent !== null) {
                this.editTask(taskId, newTaskContent);
            }
        } else if (target.classList.contains('delete-btn')) {
            this.deleteTask(taskId);
        } else if (target.classList.contains('complete-btn')) {
            this.markCompleted(taskId);
        }
    }

    addTask(content) {
        const task = {
            id: this.currentId++,
            content: content,
            completed: false
        };
        this.tasks.push(task);
        this.renderTasks();
    }

    editTask(taskId, newTask) {
        if (this.tasks[taskId]) {
            this.tasks[taskId].content = newTask;
            this.renderTasks();
        }
    }

    deleteTask(taskId) {
        this.tasks.splice(taskId, 1);
        this.renderTasks();
    }

    markCompleted(taskId) {
        if (this.tasks[taskId]) {
            this.tasks[taskId].completed = true;
            this.renderTasks();
        }
    }

    renderTasks() {
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';
        this.tasks.forEach(task => {
            const taskElement = document.createElement('li');
            taskElement.innerHTML = `
                <span>${task.completed ? '\u2713' : '\u274C'} ${task.content}</span>
                <button data-id='${task.id}' class='edit-btn'>Edit</button>
                <button data-id='${task.id}' class='delete-btn'>Delete</button>
                <button data-id='${task.id}' class='complete-btn'>Complete</button>
            `;
            taskList.appendChild(taskElement);
        });
    }

    changeTheme(theme) {
        const root = document.documentElement;
        if (theme === 'dark') {
            root.style.setProperty('--bg-color', '#333');
            root.style.setProperty('--text-color', '#fff');
            root.style.setProperty('--button-color', '#555');
        } else {
            root.style.setProperty('--bg-color', '#fff');
            root.style.setProperty('--text-color', '#000');
            root.style.setProperty('--button-color', '#ccc');
        }
    }
}

const todoApp = new TodoApp();