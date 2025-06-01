import { Component, inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CreateTask, Task } from '../../services/task-service';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-edit-dialog',
  imports: [
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    CommonModule
  ],
  templateUrl: './edit-dialog.html',
  styleUrl: './edit-dialog.scss'
})
export class EditDialog {
  public dialogRef = inject(MatDialogRef<EditDialog>);
  private fb = inject(FormBuilder);
  readonly data = inject<Task>(MAT_DIALOG_DATA);

  form: FormGroup = this.fb.group({
    title: [this.data?.title || '', Validators.required],
    description: [this.data?.description || '', Validators.required],
    status: [this.data?.status || 'todo', Validators.required],
    priority: [this.data?.priority || 'low', Validators.required],
    user_id: [this.data?.user_id || null, Validators.required]
  });
  

  onCancel() {
    this.dialogRef.close();
  }

  onSave() {
    if (this.form.invalid) return;
    const updatedTask = this.data && 'id' in this.data
      ? { ...this.data, ...this.form.value }
      : this.form.value as CreateTask;
    this.dialogRef.close(updatedTask);
  }
}
