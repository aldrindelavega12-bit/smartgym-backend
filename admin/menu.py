from admin.actions import (
    add_member,
    add_walkin,
    process_payment,
    pay_locker_overtime,
    clear_fingerprint,
    delete_member,
    delete_walkin,
    view_members,
    view_walkins
)


def admin_menu(in_fp, out_fp, ui):
    while True:
        print("\n===== SMART GYM ADMIN MENU =====")
        print("1. Add Member")
        print("2. Add Walkin")
        print("3. Payment")
        print("4. Pay Locker Overtime")   # NEW
        print("5. Clear Fingerprint")
        print("6. Delete Member")
        print("7. Delete Walkin")
        print("8. View Members")
        print("9. View Walkins")
        print("0. Exit")
        
        choice = input("Select option: ")

        if choice == "1":
            add_member(in_fp, out_fp, ui)
        elif choice == "2":
            add_walkin(in_fp, out_fp, ui)
        elif choice == "3":
            process_payment()
        elif choice == "4":
            pay_locker_overtime()
        elif choice == "5":
            clear_fingerprint(in_fp, out_fp)
        elif choice == "6":
            delete_member(in_fp, out_fp)
        elif choice == "7":
            delete_walkin(in_fp, out_fp)
        elif choice == "8":
            view_members()
        elif choice == "9":
            view_walkins()
        elif choice == "0":
            print("Exiting admin mode...")
            break
        else:
            print("Invalid option.")