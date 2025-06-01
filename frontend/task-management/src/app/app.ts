import { Component } from '@angular/core';
import { TaskList } from './components/task-list/task-list';
import { Header } from './components/header/header';
import { User } from './services/user-service';

@Component({
  selector: 'app-root',
  imports: [TaskList, Header],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected title = 'task-management';
  selectedUser: User | null = null;

  onUserChanged(user: User) {
    this.selectedUser = user;
  }
}
