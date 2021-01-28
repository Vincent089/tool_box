from sqlalchemy import create_engine, text


def create_connection(db_file):
    """
    Create a connection engine with SQLAlchemy
    :param db_file:
    :return:
    """
    return create_engine('sqlite:///%s' % db_file,
                         echo=True)


if __name__ == '__main__':
    e = create_connection(r"C:\Users\vincent.corriveau\Documents\Workshop\tool_box\_db_repo\deviceconfig.db")
