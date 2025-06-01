import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditDialog } from './edit-dialog';

describe('EditDialog', () => {
  let component: EditDialog;
  let fixture: ComponentFixture<EditDialog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDialog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
