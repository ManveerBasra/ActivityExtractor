import codecs


def output_activity(service, activity_list):
    """
    Outputs viewing activity into 'SERVICE_activity.txt'
    """
    print('Writing activity to \'%s_activity.txt\'' % service.lower())
    # Open output file
    file = codecs.open('%s_activity.txt' % service.lower(), 'w+', encoding='utf8')
    # Write to file
    for item in activity_list:
        file.write(item)

    # Close output file
    file.close()
    print('Process finished')
