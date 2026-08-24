def delete_fingerprint(fp_manager, fp_id):

    print(f"[FP] Deleting slot {fp_id} from IN")

    fp_manager.delete_in(fp_id)

    print(f"[FP] Deleting slot {fp_id} from OUT")

    fp_manager.delete_out(fp_id)

    print(f"[FP] Deleted slot {fp_id} from both sensors")

    return True