import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsedComponent } from './used.component';

describe('UsedComponent', () => {
  let component: UsedComponent;
  let fixture: ComponentFixture<UsedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsedComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UsedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
